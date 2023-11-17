from random import randint
from rest_framework import status, permissions, views, response
from rest_framework.authtoken.models import Token
from .payment import client, client_receipt
from .utils import verify
from .serializers import UserSerializer, ParentSerializer, AgeSerializer, StudentClassSerializer
from .models import User, VerifyPhone, Parent, StudentClass, Payment, Age
from .permissions import IsParentUser
from course.models import Subject, Lesson, StudentSubject, StudentLesson


class PaymentAPI(views.APIView):
    def get(self, request):
        obj = Payment.objects.first()
        return response.Response({'success': obj.method})


class ClassAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        qs = StudentClass.objects.all()
        serializer = StudentClassSerializer(qs, many=True)
        return response.Response({'success': True, 'result': serializer.data})


class AgeAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        qs = Age.objects.all()
        serializer = AgeSerializer(qs, many=True)
        return response.Response({'success': True, 'result': serializer.data})


class CardCreate(views.APIView):
    def post(self, request, *args, **kwargs):
        res = client.cards_create(number=self.request.data['number'], expire=self.request.data['expire'], save=False)
        try:
            token = res['result']['card']['token']
        except Exception as e:
            print(e)
            return response.Response({'data': {'message': res['error']['message']}}, status=status.HTTP_400_BAD_REQUEST)
        client.card_get_verify_code(token)
        return response.Response(
            {'data': {'success': True, 'result': {'message': 'Verification code has sent', 'token': token}}})


class CardVerify(views.APIView):
    def post(self, request, *args, **kwargs):
        res = client.cards_verify(self.request.data['code'], self.request.data['token'])
        try:
            token = res['result']['card']['token']
        except Exception as e:
            print(e)
            return response.Response({'data': {'success': False, 'message': res['error']['message']}},
                                     status=status.HTTP_400_BAD_REQUEST)
        check = client.cards_check(token)
        if check['result']['card']['verify']:
            return response.Response({'data': {'success': True, 'result': {'message': "Card verified successfully"}}})
        else:
            return response.Response({'data': {'success': False, 'message': check['error']['message']}},
                                     status=status.HTTP_400_BAD_REQUEST)


class ReceiptCreateStudent(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        summa = 0
        subject = Subject.objects.filter(id=self.request.data['subject']).first()
        for i in self.request.data['themes']:
            lesson = Lesson.objects.filter(id=i).first()
            summa += lesson.price
        res = client_receipt.receipts_create(subject.id, float(summa * 100), self.request.user.id, subject.name)
        try:
            invoice_id = res['result']['receipt']['_id']
        except Exception as e:
            print(e)
            return response.Response({'data': {'success': False, 'message': res['error']['message']}},
                                     status=status.HTTP_400_BAD_REQUEST)
        pay = client_receipt.receipts_pay(subject.id, invoice_id, self.request.data['token'], self.request.user.phone)
        try:
            pay['result']['receipt']['_id']
        except Exception as e:
            print(e)
            return response.Response({'data': {'success': False, 'message': pay['error']['message']}},
                                     status=status.HTTP_400_BAD_REQUEST)
        st_sb = StudentSubject.objects.filter(user=self.request.user, subject=subject).first()
        if st_sb:
            student_subject = st_sb
        else:
            student_subject = StudentSubject.objects.create(user=self.request.user, subject=subject)
        for i in self.request.data['themes']:
            lesson = Lesson.objects.filter(id=i).first()
            StudentLesson.objects.create(subject=student_subject, lesson=lesson)
        return response.Response({'success': True, 'result': {'message': 'Your payment was made successfully'}})


class ReceiptCreateParent(views.APIView):
    permission_classes = [IsParentUser]

    def post(self, request, *args, **kwargs):
        summa = 0
        for i in self.request.data['themes']:
            th = Lesson.objects.filter(id=i).first()
            summa += th.price
        subject = Subject.objects.filter(id=self.request.data['subject']).first()
        res = client_receipt.receipts_create(subject.id, float(summa * 100), self.request.data['student_id'],
                                             subject.name)
        try:
            invoice_id = res['result']['receipt']['_id']
        except Exception as e:
            print(e)
            return response.Response({'data': {'success': False, 'message': res['error']['message']}},
                                     status=status.HTTP_404_NOT_FOUND)
        pay = client_receipt.receipts_pay(subject.id, invoice_id, self.request.data['token'], self.request.user.phone)
        try:
            pay['result']['receipt']['_id']
        except Exception as e:
            print(e)
            return response.Response({'data': {'success': False, 'message': res['error']['message']}},
                                     status=status.HTTP_400_BAD_REQUEST)

        st_sb = StudentSubject.objects.filter(user_id=self.request.data['student_id'], subject=subject).first()
        if st_sb:
            student_subject = st_sb
        else:
            student_subject = StudentSubject.objects.create(user_id=self.request.data['student_id'], subject=subject)
        for i in self.request.data['themes']:
            lesson = Lesson.objects.filter(id=i).first()
            StudentLesson.objects.create(subject=student_subject, lesson=lesson)
        return response.Response({'data': {'success': True, 'result': {'message': 'OK'}}})


class ApplePayStudent(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subject = Subject.objects.filter(id=self.request.data['subject']).first()
        st_sb = StudentSubject.objects.filter(user=self.request.user, subject=subject).first()
        if st_sb:
            student_subject = st_sb
        else:
            student_subject = StudentSubject.objects.create(user=self.request.user, subject=subject)
        for lesson in subject.lessons.all():
            StudentLesson.objects.create(subject=student_subject, lesson=lesson)
        return response.Response({'success': True, 'result': {'message': 'Your payment was made successfully'}})


class ApplePayParent(views.APIView):
    permission_classes = [IsParentUser]

    def post(self, request, *args, **kwargs):
        subject = Subject.objects.filter(id=self.request.data['subject']).first()
        st_sb = StudentSubject.objects.filter(user_id=self.request.data['student_id'], subject=subject).first()
        if st_sb:
            student_subject = st_sb
        else:
            student_subject = StudentSubject.objects.create(user_id=self.request.data['student_id'], subject=subject)
        for lesson in subject.lessons.all():
            StudentLesson.objects.create(subject=student_subject, lesson=lesson)
        return response.Response({'data': {'success': True, 'result': {'message': 'OK'}}})


class ParentAPI(views.APIView):
    permission_classes = [IsParentUser]

    def get(self, request, *args, **kwargs):
        qs = Parent.objects.filter(user=self.request.user)
        ls = list()
        for i in qs:
            ls.append(ParentSerializer(instance=i).data)
        return response.Response({'success': True, 'result': ls})


class SearchAPI(views.APIView):
    permission_classes = [IsParentUser]

    def post(self, request, *args, **kwargs):
        child = User.objects.filter(phone__exact=self.request.data['phone']).first()
        obj = Parent.objects.filter(user=self.request.user, children=child).first()
        if (child == self.request.user) or (child is None) or (obj is not None):
            return response.Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        elif child:
            serializer = UserSerializer(child).data
            return response.Response({'success': True, 'result': serializer})


class RequestToJoinAPI(views.APIView):
    permission_classes = [IsParentUser]

    def post(self, request):
        # code = randint(10000, 100000)
        code = '77777'
        verify(self.request.data['phone'], code)
        VerifyPhone.objects.create(phone=self.request.data['phone'], code=code)
        return response.Response(
            {'success': True, 'result': {'message': 'Verification code was sent to your child phone'}})


class RequestToJoinVerifyAPI(views.APIView):
    permission_classes = [IsParentUser]

    def post(self, request, *args, **kwargs):
        v = VerifyPhone.objects.filter(phone=self.request.data['phone'], code=self.request.data['code']).first()
        if v:
            child = User.objects.filter(phone=self.request.data['phone']).first()
            Parent.objects.create(user=self.request.user, children=child)
            v.delete()
        else:
            return response.Response({'success': False, 'message': "Verification code incorrect"},
                                     status=status.HTTP_400_BAD_REQUEST)
        return response.Response({'success': True, 'result': {'message': "Your child joined"}})


class LoginAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        # kod = randint(10000, 100000)
        code = '77777'
        verify(self.request.data['phone'], code)
        VerifyPhone.objects.create(phone=self.request.data['phone'], code=code)
        user = User.objects.filter(phone=self.request.data['phone']).first()
        if user is None:
            user = User.objects.create_user(phone=self.request.data['phone'], password='1')
            Token.objects.create(user=user)
            return response.Response(
                {'success': True, 'result': {'message': 'User registered verification code was sent to your phone',
                                             'is_registered': True}},
                status=status.HTTP_201_CREATED)
        elif user.is_verified:
            return response.Response({'success': True,
                                      'result': {'message': 'Verification code was sent to your phone',
                                                 'is_registered': False}})
        else:
            return response.Response(
                {'success': True, 'result': {'message': 'User registered verification code was sent to your phone',
                                             'is_registered': True}}, status=status.HTTP_201_CREATED)


class VerifyPhoneAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        v = VerifyPhone.objects.filter(phone=self.request.data['phone'], code=self.request.data['code']).first()
        if v:
            user = User.objects.filter(phone=self.request.data['phone']).first()
            v.delete()
            token = Token.objects.get(user=user)
            return response.Response({'success': True, 'result': {'token': token.key, 'is_parent': user.is_parent}})
        else:
            return response.Response({'success': False, 'message': "Phone number or code invalid"},
                                     status=status.HTTP_400_BAD_REQUEST)


class ParentLoginAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        # code = randint(10000, 100000)
        code = '77777'
        verify(self.request.data['phone'], code)
        VerifyPhone.objects.create(phone=self.request.data['phone'], code=code)
        user = User.objects.filter(phone=self.request.data['phone']).first()
        if user is None:
            user = User.objects.create_user(phone=self.request.data['phone'], password='1')
            user.is_parent = True
            user.save()
            Token.objects.create(user=user)
            return response.Response(
                {'success': True, 'result': {'message': 'User registered verification code was sent to your phone',
                                             'is_registered': True}},
                status=status.HTTP_201_CREATED)
        elif user.is_verified:
            return response.Response({'success': True,
                                      'result': {'message': 'Verification code was sent to your phone',
                                                 'is_registered': False}})
        else:
            return response.Response(
                {'success': True, 'result': {'message': 'User registered verification code was sent to your phone',
                                             'is_registered': True}}, status=status.HTTP_201_CREATED)


class UserAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=self.request.user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.request.user.is_verified = True
        self.request.user.save()
        return response.Response({'success': True, 'result': serializer.data})

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=self.request.user)
        return response.Response({'success': True, 'result': serializer.data})

    def delete(self, request, *args, **kwargs):
        self.request.user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
