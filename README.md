# Medium Blogs in README

**Basic idea of this is to show what you have written in Medium in your Github README for a given period.**

![Example](https://user-images.githubusercontent.com/31571237/92688701-6dec5600-f35b-11ea-8b4d-10085fda9530.PNG)

### Update your README

Add the comment below your README.md
```
<!--START_SECTION:medium-->
<!--END_SECTION:medium-->
```
The list will be between the these two sections.

### Create a workflow


> **If you're executing the workflow on your Profile repository (`<username>/<username>`), You don't need a GitHub access token. If not create a [Github access token](https://docs.github.com/en/actions/configuring-and-managing-workflows/authenticating-with-the-github_token) and add it to secret with the name GH_TOKEN**

```
on:
  schedule:
      # Runs at every 2 days. Schedule it as you want.
      - cron: '0 0 */2 * *'
jobs:  
  update-readme:
    name: Update this repo's README
    runs-on: ubuntu-latest
    steps:
      - uses: wathsara/medium-blogs-readme@master
        with:
          MEDIUM_HANDLER: '@wathsara' //Your Medium Handler
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          REPOSITORY: <username>/<repo>
          DAYS: 30 // Show blogs wrote in last 30 days
```

