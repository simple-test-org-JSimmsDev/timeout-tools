# Locally (Mac)

1. Setup your tokens
    ```bash
    export GITHUB_TOKEN=<your_personal_access_token>
    export GITHUB_ORG=<your_organization_name>
    ```

2. Install dependencies 
    ```
    pip install PyGithub
    ```

3. Run the script
    ```
    python script.py <repository_name> <language>
    ```

# Locally (Windows - CMD)

1. Setup your tokens
    ```bash
    set GITHUB_TOKEN=<your_personal_access_token>
    set GITHUB_ORG=<your_organization_name>
    ```

2. Install dependencies 
    ```
    pip install PyGithub
    ```

3. Run the script
    ```
    python script.py <repository_name> <language>
    ```

# Dockerized

Note of preference to using the Docker version for compatability

1. Build the image
   ```bash
   docker build -t github-repo-creator .
   ```

2. Run and pass through token & command
   ```bash
   docker run --rm -e GITHUB_TOKEN=<YOUR_GITHUB_TOKEN> -e GITHUB_ORG=<YOUR_GITHUB_ORG> github-repo-creator python script.py <GITHUB_REPOSITORY_NAME> <CHOOSEN_LANGUAGE>
   ```
