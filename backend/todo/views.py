
from rest_framework import serializers, viewsets, permissions
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Todo
		fields = ["id", "title", "description", "completed", "created_at", "updated_at"]


class TodoViewSet(viewsets.ModelViewSet):
	serializer_class = TodoSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Todo.objects.filter(user=self.request.user).order_by("-created_at")

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
