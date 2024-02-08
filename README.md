# TIMI

## Sommaire

- [Introduction](#introduction)
- [Collaborateurs](#collaborateurs)
- [Capacité du robot](#capacité-du-robot)
- [Structure du code](#structure-du-code)

## Introduction

Dans le cadre de notre projet Réseaux, nous avons dû implémenter du code à l'aide de la librairie MQTT pour permettre à notre Raspberry Pi 5 de participer à une capture de drapeau. Le but était de pouvoir entrer dans une zone, y rester un temps défini, puis de scanner un QR Code. Il fallait également ajouter une capacité de tir et de réception de lumières infrarouges. Le nom
donné à notre robot est **TIMI**.

## Collaborateurs

- [Ilyes DJERFAF (ISD)](https://github.com/ilyesdjerfaf)
- [Ilan ALIOUCHOUCHE (ISD)](https://github.com/ilanaliouchouche)
- [Marwan KHAIRALLAH (IOT)](https://github.com/Marwankhairallah)
- [Tarek ATBI (ISD)](https://github.com/tarekatbi)

## Capacité du robot

| Capacité             | Description |
|----------------------|-------------|
| Utilisation d'une manette *PS5*s| À l'aide de PyDualSense, nous pouvons contrôler notre robot sans fil avec une manette de PS5. |
| Déplacements         | Grâce à notre manette, nous avons un large choix de déplacements, des accélérations, des mouvements plus lents pour être plus précis, etc. |
| Tir et Réception     | Nous pouvons tirer avec le robot via notre manette. De plus, nous pouvons détecter si nous sommes touchés ainsi que l'identité du responsable. |
| Détection de QR Code | Nous pouvons prendre une photo (toujours via la manette) et détecter le QR Code. |
| Détection de la zone | Le robot détecte très bien s'il est dans la zone du drapeau, renvoyant au serveur ses entrées et sorties. |
| Son                  | Chaque action renvoie un son particulier (via MQTT). Par exemple, lorsqu'on tire ou réussit à scanner le QR Code. On retrouve même un mode disco mettant une musique et jouant sur les LED. |
| Connexion et interaction avec le serveur | Toutes les actions sont publiées et envoyées sur le serveur, elles sont toutes visibles au bon endroit. |

On a donc un robot qui fait tout ce qu'il doit faire, et prêt pour des captures de drapeaux. On retrouve, en plus, beaucoup de mobilités gérées avec la manette ainsi que des animations qui viennent complétées les actions de base.

## Structure du code

| Folder | Description |
|--------------|-------------|
| `local`      | Ce dossier contient le code exécuté localement pour écouter les messages sur le serveur et exécuter les différents sons. Il inclut les fichiers sons et le fichier `subsong.py`. |
| `robot`      | Ce dossier représente tout le code nécessaire au robot ainsi qu'au serveur. Le fichier principal est `timi.py`, où on retrouve l'implémentation de toutes les interactions. |

