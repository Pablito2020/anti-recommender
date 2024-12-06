# Spotify Antirecommender system

## Configure spotify api for devs

Go to the [spotify for devs url](https://developer.spotify.com/dashboard) and create a new app. Be aware that you have to put the correct redirect link.

## El Despatx credentials

Our credentials for the project live inside the credentials file, which is encrypted with [git-crypt](https://github.com/AGWA/git-crypt) with our own gpg keys. So, if you're one of the main developers, you can see the files with:

```bash
$ git-crypt unlock
```

## Developement environment

We use [nix](https://nixos.org/) as the build tool of the project. You can use the developement environment we provide with:

```
$ nix develop
```
