!function() {
    const Types = { Unknown: 0, Tenor: 1, Discord: 2, DiscordExternal: 3 };

    const isTenorRegex = /tenor\.com/;
    const tenorIdRegex = /\d+$/;
    // Example URL: https://cdn.discordapp.com/attachments/12345/67890/test.gif
    const discordUrlRegex = /https:\/\/(cdn|media).discordapp.(com|net)\/\S+/;
    const discordExternalUrlRegex = /https:\/\/images-ext-2.discordapp.(com|net)\/(?<query>(?!https])\S+)(?<resource>(https|http)\S+)/i;

    window.addEventListener('load', () => {


        const type = getType();
        switch(type) {
            case Types.Tenor:
                embedTenor();
                break;
            case Types.Discord:
                embedDiscord();
                break;
            case Types.DiscordExternal:
                embedDiscordExternal();
                break;
            default:
                break;
        }

    });

    function getType() {
        if (isTenorRegex.test(location.href)) {
            return Types.Tenor;
        }
        if (discordUrlRegex.test(location.href)) {
            return Types.Discord
        }
        if (discordExternalUrlRegex.test(location.href)) {
            return Types.DiscordExternal;
        }

        return Types.Unknown;
    }

    function embedTenor() {
        const regexResult = location.href.match(tenorIdRegex);
        const id = regexResult[0];

        if (!id) {
            document.body.innerHTML += "<p style='color: red;'>Could not get a tenor id from the url!!</p>";
            return;
        }

        document.body.classList.add('tenor');
        document.body.innerHTML += `<iframe allowtransparency="true" allowfullscreen="true" scrolling="no" style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://tenor.com/embed/${id}?canonicalurl=" frameborder="0"></iframe>`
    }

    function embedDiscord() {
        const exec = discordUrlRegex.exec(location.href);
        if (!exec) {
            document.body.innerHTML += "<p style='color: red;'>Could not get discord link from url!!</p>";
            return;
        }
        const url = exec[0];
        embedDiscordResource(url)
    }

    function embedDiscordExternal() {
        const exec = discordExternalUrlRegex.exec(location.href);
        if (!exec) {
            document.body.innerHTML += "<p style='color: red;'>Could not get external discord link from url!!</p>";
            return;
        }
        let url = exec.groups.resource;
        const queryParts = exec.groups.query.split('/');
        const query = decodeURIComponent(queryParts[queryParts.length - 2] ?? '');

        if (url.startsWith('https/')) {
            url = `https://${url.substring(6)}`;
        } else if (url.startsWith('http/')) {
            url = `https://${url.substring(5)}`
        }

        url += `${query}`;

        embedDiscordResource(url);
    }

    function embedDiscordResource(url) {
        let fileExtension = url.split('.');
        fileExtension = fileExtension[fileExtension.length - 1].split('?')[0];

        const images = ['jpg', 'jpeg', 'png', 'gif'];
        const videos = ['mp4', 'webm'];
        const audio = ['mp3', 'wav'];

        document.body.classList.add('discord');
        if (videos.includes(fileExtension)) {
            embedVideo(url, fileExtension);
        } else if (images.includes(fileExtension)) {
            embedImage(url);
        } else if (audio.includes(fileExtension)) {
            embedAudio(url, fileExtension);
        }
    }

    function embedVideo(url, type) {
        document.body.innerHTML += `<video controls autoplay><source src="${url}" type="video/${type}" ></video>`;
    }

    function embedImage(url) {
        document.body.innerHTML += `<img src="${url}" alt="image!" />`;
    }

    function embedAudio(url, type) {
        document.body.innerHTML += `<audio controls><source src="${url}" type="audio/${type}"></audio>`;
    }
}();
