# timeout-tools
Tools Test Repository - For timeout take home challenge

# Requirements

1. Input of: Application name, the programming language  ✔
2. Outputs: Repository of the github, with a standardized name  ✔
3. Contain sensible default files  ✔
4. Engineers team added to repo  ✔
5. Branch protection rules (Sensible)  ✔

# Points of note

1. I imagined this as a repository of tools, as such I have put the actual script under github-creation-script (Please ensure your directory is in the correct location when running)

2. Local version, and Dockerized version for quick demonstration purposes, both work (Operating System issues with local aside)

3. This checks your local environment file, you can explicitly pass it to the image (IMPORTANT: We try to avoid baking any credentials into containers, in memory is safer when ran in app via secret store/manager, etc)

4. Included an example, and working python application with a relevant structure to demonstrate it working (Also local, and dockerized)

5. Each project has an appropriate readme to assist with running - anything odd happenning? Feel free to reach out to me.

6. I like the idea of having your explicit files ready in your file templates - E.g. having a standard language, with room to add more, say you want a language with a template build, like java standalone, then a java springboot template, this allows that

7. Adding security scanners to look for keys and sensitive information via regex/tooling, just incase something gets added to a template where it shouldn't

8. I haven't been able to test if the configuring rules works as the API throws me to the below error as a response, see documentation also outlining this, please feel free to try it out on your side.

error: 403 {"message": "Upgrade to GitHub Pro or make this repository public to enable this feature.", "documentation_url": "https://docs.github.com/rest/branches/branch-protection#update-branch-protection", "status": "403"}