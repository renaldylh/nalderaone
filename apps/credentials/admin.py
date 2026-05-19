import json
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin

from .models import PlatformCredential


class PlatformCredentialForm(forms.ModelForm):
    credentials_json = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "cols": 60, "style": "font-family: monospace;"}),
        help_text="Format JSON. Contoh Meta: {\"app_id\": \"123\", \"app_secret\": \"abc\"}",
        required=False,
        label="Credentials (JSON)"
    )

    class Meta:
        model = PlatformCredential
        fields = ["organization", "platform", "is_configured", "credentials_json"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate the form field with the decrypted credentials as pretty JSON
            self.fields["credentials_json"].initial = json.dumps(self.instance.credentials, indent=2)

    def clean_credentials_json(self):
        data = self.cleaned_data.get("credentials_json")
        if not data:
            return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Format JSON tidak valid: {e}")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.credentials = self.cleaned_data["credentials_json"]
        if commit:
            instance.save()
        return instance


@admin.register(PlatformCredential)
class PlatformCredentialAdmin(admin.ModelAdmin):
    form = PlatformCredentialForm
    list_display = ("organization", "platform", "is_configured", "test_result", "tested_at")
    list_filter = ("platform", "is_configured", "test_result")
    search_fields = ("organization__name",)
    readonly_fields = ("id", "created_at", "updated_at", "tested_at")

