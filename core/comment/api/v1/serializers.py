from rest_framework import serializers
from ...models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'reply_to', 'name', 'email', 'message']
        read_only_fields = ['id']

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment message cannot be empty.")
        return value
