Locally (Mac)

1. Setup your tokens
    ```bash
    export GITHUB_TOKEN=<your_personal_access_token>
    export GITHUB_ORG=<your_organization_name>
    ```

2. Install dependencies 
    ```bash
    pip install PyGithub
    ```

3. Run the script
    ```bash
    python script.py <repository_name> <language>
    ```

Locally (Windows - CMD)

1. Setup your tokens
    ```bash
    set GITHUB_TOKEN=<your_personal_access_token>
    set GITHUB_ORG=<your_organization_name>
    ```

2. Install dependencies 
    ```bash
    pip install PyGithub
    ```

3. Run the script
    ```bash
    python script.py <repository_name> <language>
    ```

Dockerized

docker build -t github-repo-creator .

docker run --rm -e GITHUB_TOKEN=<your_github_token> -e GITHUB_ORG=<your_org_name> github-repo-creator <app_name> <language>
