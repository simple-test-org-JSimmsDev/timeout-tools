import os
import subprocess
from github import Github

# load environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG", "my-org")
DEFAULT_TEAM = "Engineers"

# validate environment variables
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in the environment.")

g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG_NAME)

def create_github_repository(app_name, language):
    """
    Creates a GitHub repository with standardized settings and files for the given application.

    :param app_name: Name of the application (repository name).
    :param language: Programming language (currently only Python).
    """
    # standardize the appname
    repo_name = app_name.lower().replace(" ", "-")

    repo = org.create_repo(
        name=repo_name,
        description=f"Repository for {app_name} - {language} application.",
        private=True
    )

    print(f"Repository '{repo_name}' created successfully.")

    language_template_path = os.path.join("languages", language.lower())
    if not os.path.exists(language_template_path):
        raise FileNotFoundError(f"Language template folder not found: {language_template_path}")

    for root, _, files in os.walk(language_template_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, language_template_path).replace(os.sep, "/")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "rb") as f:
                    content = f.read().decode("latin-1")
            repo.create_file(
                path=relative_path,
                message=f"Add default file: {file}",
                content=content
            )


    print("Default files added.")

    # team permissions
    team = next((t for t in org.get_teams() if t.name == DEFAULT_TEAM), None)
    if team:
        team.add_to_repos(repo)
        print(f"Added team '{DEFAULT_TEAM}' to repository.")
    else:
        print(f"Team '{DEFAULT_TEAM}' not found.")

    # branch protection rules (Requires premium/enterprise, can't fully test myself)
    try:
        branch = repo.get_branch("main")
        branch.edit_protection(
            required_approving_review_count=1,
            dismiss_stale_reviews=True,
            enforce_admins=True
        )
        print("Branch protection rules set.")
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
