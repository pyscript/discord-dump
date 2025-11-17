# PyScript Discord Dump (2025-11-17)

This repository contains a dump of all the *public channels* that were deleted in a Discord server cleanup on 2025-11-17.

Each channel has an associated HTML file with the name: `PyScript_SUB_SECTION-server-name_1234567` (where `1234567` is the channel's unique ID). The original un-changed HTML files can be found inthe `original_html` directory.

Each channel was extracted using the [Discord Channel Exporter](https://github.com/Tyrrrz/DiscordChatExporter) utility, and then post-processed so that all images and other assets stored in Discord's CDN were downloaded into the `assets` directory in the repository. The HTML files were further updated so the URLs pointing to such assets pointed to the locally archived versions.

The script to do this work can be found in `post_process.py`. This requires the `beautifulsoup` and `requests` packages to work.

That's it.