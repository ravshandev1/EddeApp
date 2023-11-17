from rest_framework import response, views, permissions
from . import serializers
from . import models


class SubjectListAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        for i in models.Subject.objects.all():
            if not models.Wishlist.objects.filter(user=self.request.user, subject=i):
                ls.append(serializers.SubjectSerializer(instance=i).data)
        return response.Response({'success': True, 'result': ls})


class SubjectsAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        qs = models.Subject.objects.all()
        serializer = serializers.SubjectSerializer(qs, many=True).data
        return response.Response({'success': True, 'result': serializer})


class WishlistView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # cnt = 0
        # for i in Subject.objects.all():
        # st_sb = StudentSubject.objects.filter(user=user, subject=i).first()
        # for j in i.subject_theme.all():
        # if StudentTheme.objects.filter(theme=j, subject=st_sb).first() is not None:
        # cnt += 1
        # if cnt == i.subject_theme.all().count():
        # Wishlist.objects.filter(user=user, subject=i).delete()
        # cnt = 0
        ls = list()
        qs = models.Wishlist.objects.filter(user=self.request.user)
        for i in qs:
            ls.append(serializers.SubjectSerializer(instance=i.subject).data)
        return response.Response({'success': True, 'result': ls})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        for i in self.request.data['subjects']:
            if models.Wishlist.objects.filter(user_id=user.id, subject_id=i).first():
                pass
            else:
                models.Wishlist.objects.create(user_id=user.id, subject_id=i)
        return response.Response(
            {'success': True, 'result': {'message': "Subject successfully added to your wishlist!"}})

    def delete(self, request, *args, **kwargs):
        models.Wishlist.objects.filter(user=self.request.user, subject_id=self.request.data['subject']).delete()
        return response.Response(
            {'success': True, 'result': {'message': "Subject successfully deleted in your wishlist!!"}})


class LevelView(views.APIView):
    def get(self, request, *args, **kwargs):
        ls = list()
        ls.append({'name': "All"})
        for i in models.Level.objects.all():
            ls.append(serializers.LevelSerializer(instance=i).data)
        return response.Response({'success': True, 'result': ls})


class StudentSubjectAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        is_complete = self.request.query_params.get('is_completed', None)
        ls = list()
        for i in models.StudentSubject.objects.filter(user=self.request.user):
            if is_complete == 'true':
                if i.percent == 100:
                    ls.append(serializers.StudentSubjectSerializer(i).data)
            elif is_complete == 'false':
                if i.percent < 100:
                    ls.append(serializers.StudentSubjectSerializer(i).data)
        if is_complete:
            return response.Response({'success': True, 'result': ls})
        else:
            return response.Response({'success': False})


class ParentSubjectAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        is_complete = self.request.query_params.get('is_completed', None)
        ls = list()
        for i in models.StudentSubject.objects.filter(user_id=self.request.query_params.get('user_id')):
            if is_complete == 'true':
                if i.percent == 100:
                    ls.append(serializers.StudentSubjectSerializer(i).data)
            elif is_complete == 'false':
                if i.percent < 100:
                    ls.append(serializers.StudentSubjectSerializer(i).data)
        if is_complete:
            return response.Response({'success': True, 'result': ls})
        else:
            return response.Response({'success': False})


class SubjectDetailAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = self.request.query_params.get('level', None)
        subject = models.Subject.objects.filter(id=self.kwargs.get('pk')).first()
        student_subject = models.StudentSubject.objects.filter(user=self.request.user, subject=subject).first()
        ls = list()
        if level:
            cnt = 0
            level = models.Level.objects.filter(name__exact=level).first()
            for lesson in subject.lessons.filter(level_id__exact=level.id):
                data = serializers.LessonSerializer(lesson).data
                les = models.StudentLesson.objects.filter(subject=student_subject, lesson=lesson).first()
                if les:
                    data['is_paid'] = True
                    data['is_view'] = les.is_view
                elif cnt < 2:
                    data['is_paid'] = True
                    data['is_view'] = False
                    cnt += 1
                else:
                    data['is_paid'] = False
                    data['is_view'] = False
                ls.append(data)
        else:
            cnt = 0
            for lesson in subject.lessons.all():
                data = serializers.LessonSerializer(lesson).data
                les = models.StudentLesson.objects.filter(subject=student_subject, lesson=lesson).first()
                if les:
                    data['is_paid'] = True
                    data['is_view'] = les.is_view
                elif cnt < 2:
                    data['is_paid'] = True
                    data['is_view'] = False
                    cnt += 1
                else:
                    data['is_paid'] = False
                    data['is_view'] = False
                ls.append(data)
        return response.Response({'success': True, 'result': ls})


class ParentSubjectDetailAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = self.request.query_params.get('level', None)
        user_id = self.request.query_params.get('user_id', None)
        subject = models.Subject.objects.filter(id=self.kwargs.get('pk')).first()
        st_sb = models.StudentSubject.objects.filter(user_id=user_id, subject=subject).first()
        ls = list()
        if level:
            cnt = 0
            lv = models.Level.objects.filter(name__exact=level).first()
            for lesson in subject.lessons.filter(level_id__exact=lv.id):
                dic = serializers.LessonSerializer(lesson).data
                les = models.StudentLesson.objects.filter(subject=st_sb, lesson=lesson).first()
                if les:
                    dic['is_paid'] = True
                    dic['is_view'] = les.is_view
                elif cnt < 2:
                    dic['is_paid'] = True
                    dic['is_view'] = False
                    cnt += 1
                else:
                    dic['is_paid'] = False
                ls.append(dic)
        else:
            cnt = 0
            for lesson in subject.lessons.all():
                dic = serializers.LessonSerializer(lesson).data
                les = models.StudentLesson.objects.filter(subject=st_sb, lesson=lesson).first()
                if les:
                    dic['is_paid'] = True
                    dic['is_view'] = les.is_view
                elif cnt < 2:
                    dic['is_paid'] = True
                    dic['is_view'] = False
                    cnt += 1
                else:
                    dic['is_paid'] = False
                ls.append(dic)
        return response.Response({'success': True, 'result': ls})


class DialogTextAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        lesson = models.Lesson.objects.filter(id=self.kwargs.get('pk')).first()
        serializer = serializers.DialogTextSerializer(lesson).data
        return response.Response({'success': True, 'result': serializer})


class DialogAudioAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        lesson = models.Lesson.objects.filter(id=self.kwargs.get('pk')).first()
        serializer = serializers.DialogAudioSerializer(lesson).data
        return response.Response({'success': True, 'result': serializer})


class PhraseTextAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        lesson = models.Lesson.objects.filter(id=self.kwargs.get('pk')).first()
        serializer = serializers.PhraseTextSerializer(lesson).data
        return response.Response({'success': True, 'result': serializer})


class PhraseAudioAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        lesson = models.Lesson.objects.filter(id=self.kwargs.get('pk')).first()
        serializer = serializers.PhraseAudioSerializer(lesson).data
        return response.Response({'success': True, 'result': serializer})


class DictionaryTextAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        lesson = models.Lesson.objects.filter(id=self.kwargs.get('pk')).first()
        serializer = serializers.DialogTextSerializer(lesson).data
        return response.Response({'success': True, 'result': serializer})


class DictionaryAudioAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        to_lang = self.request.query_params.get('to_lang')
        dictionary = models.Dictionary.objects.filter(lesson_id=self.kwargs.get('pk'), to_lang=to_lang).first()
        serializer = serializers.DictionaryAudioSerializer(dictionary).data
        return response.Response({'success': True, 'result': serializer})


class IsViewAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        obj = models.StudentLesson.objects.filter(lesson_id=self.kwargs.get('pk')).first()
        obj.is_view = True
        obj.save()
        return response.Response({'success': True, 'result': obj.is_view})
