from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ...tasks import create_comment_task
from .serializers import CommentSerializer


class CreateCommentApiView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_id = serializer.validated_data['post'].id
        reply_to = serializer.validated_data.get('reply_to')
        reply_to_id = reply_to.id if reply_to else None
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        message = serializer.validated_data['message']

        task = create_comment_task.apply_async(
            args=[post_id, reply_to_id, name, email, message]
        )

        return Response({
            'status': 'accepted',
            'task_id': task.id,
            'detail': 'Comment creation is processing in background.'
        }, status=status.HTTP_202_ACCEPTED)