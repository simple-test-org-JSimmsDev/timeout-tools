import os
import subprocess
from github import Github

# load environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG")
DEFAULT_TEAM = "Engineers"

# validate environment variables
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in environment.")
if not ORG_NAME:
    raise ValueError("GITHUB_ORG is not set in environment.")

g = Github(GITHUB_TOKEN)
try:
    org = g.get_organization(ORG_NAME)
except Exception as e:
    raise ValueError(f"Failed to access org '{ORG_NAME}': {e}")

def list_available_languages():
    """
    Lists all available language templates.
    """
    language_dir = "languages"
    if not os.path.exists(language_dir):
        raise FileNotFoundError(f"The language templates directory '{language_dir}' does not exist.")
    return [d for d in os.listdir(language_dir) if os.path.isdir(os.path.join(language_dir, d))]

def validate_language(language):
    """
    Validates that the specified language has a template available.
    """
    language_template_path = os.path.join("languages", language.lower())
    if not os.path.exists(language_template_path):
        available_languages = list_available_languages()
        raise ValueError(
            f"Language '{language}' is not supported. Available languages: {', '.join(available_languages)}"
        )
    return language_template_path

def check_file_size(file_path, max_size_mb=5):
    """
    Checks if a file exceeds the maximum allowed size.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(file_path) > max_size_bytes:
        raise ValueError(f"File '{file_path}' exceeds the maximum size of {max_size_mb} MB.")

def create_github_repository(app_name, language):
    """
    Creates a GitHub repository with standardized settings and files for the given application.

    :param app_name: Name of the application (repository name).
    :param language: Programming language (currently only Python).
    """
    # standardize the appname
    repo_name = app_name.lower().replace(" ", "-")

    # validate language
    language_template_path = validate_language(language)

    # create repository
    try:
        repo = org.create_repo(
            name=repo_name,
            description=f"Repository for {app_name} - {language} application.",
            private=False,
            has_issues=True,
            has_wiki=False,
            allow_merge_commit=False,
            allow_squash_merge=True
        )
    except Exception as e:
        raise ValueError(f"Failed to create repository '{repo_name}': {e}")

    print(f"Repository '{repo_name}' created successfully.")

    print(f"Repository URL: {repo.html_url}")

    # default files
    try:
        for root, _, files in os.walk(language_template_path):
            for file in files:
                file_path = os.path.join(root, file)
                check_file_size(file_path)
                relative_path = os.path.relpath(file_path, language_template_path).replace(os.sep, "/")
                try:
                    # attempt to read the file as UTF-8
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    #  UTF-8 decoding fails, read in binary mode and decode
                    print(f"Warning: File '{file_path}' is not UTF-8 encoded. Attempting fallback decoding.")
                    with open(file_path, "rb") as f:
                        content = f.read().decode("latin-1")
                repo.create_file(
                    path=relative_path,
                    message=f"Add default file: {file}",
                    content=content
                )
        print("Default files added.")
    except Exception as e:
        print(f"Error during file upload: {e}")
        print("Cleaning up partial repository creation...")
        repo.delete()
        raise ValueError(f"Repository '{repo_name}' creation failed. Partial repository cleaned up.")

    # team permissions
    try:
        team = next((t for t in org.get_teams() if t.name == DEFAULT_TEAM), None)
        if team:
            team.add_to_repos(repo)
            print(f"Added team '{DEFAULT_TEAM}' to repository.")
        else:
            print(f"Team '{DEFAULT_TEAM}' not found.")
    except Exception as e:
        print(f"Failed to add team permissions: {e}")

    # branch protection rules (Requires premium/enterprise, can't fully test myself)
    try:
        branch = repo.get_branch("main")
        branch.edit_protection(
            required_approving_review_count=1,
            dismiss_stale_reviews=True,
            enforce_admins=True,
            
            strict=True,
            require_code_owner_reviews=True,
            # Some example status checks
            # required_status_checks=[ 
            #     "continuous-integration",
            #     "tests"
            # ],
            user_push_restrictions=[],
            allow_force_pushes=False,
            allow_deletions=False
        )
        print("Enhanced branch protection rules set.")
    except Exception as e:
        print(f"Skipping branch protection setup due to error: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a GitHub repository with standard configurations.")
    parser.add_argument("name", help="Name of the application (repository).")
    parser.add_argument("language", help="Programming language (e.g., Python).")

    args = parser.parse_args()

    try:
        create_github_repository(args.name, args.language)
    except Exception as e:
        print(f"Error: {e}")
