from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.members.decorators import require_org_role
from apps.members.models import OrgMembership
from apps.credentials.models import PlatformCredential

# List of platforms that need application developer credentials.
# Mastodon (INSTANCE_OAUTH) and Bluesky (SESSION) are excluded as they are configured per-user / per-instance.
EDITABLE_PLATFORMS = [
    {
        "key": "facebook",
        "name": "Facebook",
        "id_label": "App ID",
        "secret_label": "App Secret",
        "placeholder_id": "e.g., 123456789012345",
        "placeholder_secret": "e.g., a1b2c3d4e5f6...",
    },
    {
        "key": "instagram",
        "name": "Instagram",
        "id_label": "App ID",
        "secret_label": "App Secret",
        "placeholder_id": "e.g., 123456789012345",
        "placeholder_secret": "e.g., a1b2c3d4e5f6...",
    },
    {
        "key": "instagram_login",
        "name": "Instagram (Direct)",
        "id_label": "App ID",
        "secret_label": "App Secret",
        "placeholder_id": "e.g., 123456789012345",
        "placeholder_secret": "e.g., a1b2c3d4e5f6...",
    },
    {
        "key": "threads",
        "name": "Threads",
        "id_label": "App ID",
        "secret_label": "App Secret",
        "placeholder_id": "e.g., 123456789012345",
        "placeholder_secret": "e.g., a1b2c3d4e5f6...",
    },
    {
        "key": "youtube",
        "name": "YouTube",
        "id_label": "Client ID",
        "secret_label": "Client Secret",
        "placeholder_id": "e.g., 12345-abcde.apps.googleusercontent.com",
        "placeholder_secret": "e.g., GOCSPX-...",
    },
    {
        "key": "google_business",
        "name": "Google Business Profile",
        "id_label": "Client ID",
        "secret_label": "Client Secret",
        "placeholder_id": "e.g., 12345-abcde.apps.googleusercontent.com",
        "placeholder_secret": "e.g., GOCSPX-...",
    },
    {
        "key": "linkedin_personal",
        "name": "LinkedIn (Personal Profile)",
        "id_label": "Client ID",
        "secret_label": "Client Secret",
        "placeholder_id": "e.g., 78xxxxxx",
        "placeholder_secret": "e.g., abcdefghijkl",
    },
    {
        "key": "linkedin_company",
        "name": "LinkedIn (Company Page)",
        "id_label": "Client ID",
        "secret_label": "Client Secret",
        "placeholder_id": "e.g., 78xxxxxx",
        "placeholder_secret": "e.g., abcdefghijkl",
    },
    {
        "key": "tiktok",
        "name": "TikTok",
        "id_label": "Client Key",
        "secret_label": "Client Secret",
        "placeholder_id": "e.g., awxxxxxx",
        "placeholder_secret": "e.g., abcdefghijkl",
    },
    {
        "key": "pinterest",
        "name": "Pinterest",
        "id_label": "App ID",
        "secret_label": "App Secret",
        "placeholder_id": "e.g., 123456789",
        "placeholder_secret": "e.g., abcdefghijkl",
    },
]


@login_required
@require_org_role(OrgMembership.OrgRole.ADMIN)
@require_http_methods(["GET", "POST"])
def credentials_list(request):
    org = request.org

    if request.method == "POST":
        action = request.POST.get("action")
        platform_key = request.POST.get("platform")

        if not platform_key or platform_key not in [p["key"] for p in EDITABLE_PLATFORMS]:
            messages.error(request, "Invalid platform specified.")
            return redirect("credentials:list")

        if action == "save":
            client_id = request.POST.get("client_id", "").strip()
            client_secret = request.POST.get("client_secret", "").strip()

            if not client_id or not client_secret:
                messages.error(request, "Both fields are required.")
                return redirect("credentials:list")

            # Standardize credential dictionary keys based on platform
            if platform_key == "tiktok":
                creds_dict = {
                    "client_key": client_id,
                    "client_secret": client_secret
                }
            else:
                creds_dict = {
                    "client_id": client_id,
                    "client_secret": client_secret
                }

            # Update or create the credential
            cred, created = PlatformCredential.objects.get_or_create(
                organization=org,
                platform=platform_key,
                defaults={"is_configured": True, "credentials": creds_dict}
            )
            if not created:
                cred.credentials = creds_dict
                cred.is_configured = True
                cred.save()

            display_name = next(p["name"] for p in EDITABLE_PLATFORMS if p["key"] == platform_key)
            messages.success(request, f"Credentials for {display_name} updated successfully.")
            return redirect("credentials:list")

        elif action == "delete":
            PlatformCredential.objects.filter(organization=org, platform=platform_key).delete()
            display_name = next(p["name"] for p in EDITABLE_PLATFORMS if p["key"] == platform_key)
            messages.success(request, f"Credentials for {display_name} removed successfully.")
            return redirect("credentials:list")

    # Fetch existing configurations
    db_credentials = {
        c.platform: c for c in PlatformCredential.objects.filter(organization=org)
    }

    platforms_data = []
    for p in EDITABLE_PLATFORMS:
        key = p["key"]
        db_cred = db_credentials.get(key)
        
        is_configured = False
        masked_id = ""
        masked_secret = ""
        
        if db_cred and db_cred.is_configured:
            is_configured = True
            # Get actual values to mask properly
            cid = db_cred.credentials.get("client_id") or db_cred.credentials.get("client_key") or db_cred.credentials.get("app_id") or ""
            csec = db_cred.credentials.get("client_secret") or db_cred.credentials.get("app_secret") or ""
            
            masked_id = "****" + cid[-4:] if len(cid) > 4 else "****"
            masked_secret = "****" + csec[-4:] if len(csec) > 4 else "****"

        platforms_data.append({
            **p,
            "is_configured": is_configured,
            "masked_id": masked_id,
            "masked_secret": masked_secret,
        })

    context = {
        "platforms": platforms_data,
        "settings_active": "credentials",
        "organization": org,
    }
    return render(request, "credentials/list.html", context)
