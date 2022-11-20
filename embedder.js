!function() {
    const Types = {
        Unknown: 0,
        Tenor: 1,
        Discord: 2,
        DiscordExternal: 3,
        Redgifs: 4,
    };

    const isTenorRegex = /tenor\.com/;
    const tenorIdRegex = /\d+$/;
    // Example URL: https://cdn.discordapp.com/attachments/12345/67890/test.gif
    const discordUrlRegex = /https:\/\/(cdn|media).discordapp.(com|net)\/\S+/;
    // Example URL: https://images-ext-1.discordapp.net/external/abaYIADYF/https/i.redd.it/test.jpg
    const discordExternalUrlRegex = /https:\/\/images-ext-\d.discordapp.(com|net)\/(?<query>(?!https])\S+)(?<resource>(https|http)\S+)/i;
    // Example url: https://www.redgifs.com/watch/moonlightsingingdancingcat
    const redgifsUrlRegex = /https:\/\/(www\.)?redgifs\.com\/watch\/(?<resource>\S+)/i;

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
            case Types.Redgifs:
                embedRedgifs();
                break;
            default:
                addUrlInput();
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
        if (redgifsUrlRegex.test(location.href)) {
            return Types.Redgifs;
        }

        return Types.Unknown;
    }

    function addUrlInput() {
        const basePrefix = '/just-the-thing';
        const currentUrl = (location.pathname ?? '') + (location.query ?? '') + (location.hash ?? '');
        if (currentUrl || currentUrl === basePrefix) {
            document.body.innerHTML += `<p>${currentUrl}</p>`;
        }

        document.body.innerHTML += `
<div>
  <label>URL to embed:</label>
  <br>
  <input type="text" class="url-input" name="url">
  <br>
  <p class="url-input-message"></p>
  <br>
  <button class="url-change">Embed</button>
</div>`

        const input = document.querySelector('.url-input');
        input.addEventListener('input', function() {
            if (input.value) {
                button.removeAttribute('disabled');
            } else {
                button.setAttribute('disabled', '');
            }
        });

        const button = document.querySelector('.url-change');
        button.setAttribute('disabled', '');

        // For debug purposes, set true if local.
        const isLocalHost = false;

        button.addEventListener('click', () => {
            const input = document.querySelector('.url-input');
            const hasPrefixUrl = location.pathname.startsWith(basePrefix);
            const prefix = hasPrefixUrl ? basePrefix : '/';

            const originPlusPrefix = location.origin + prefix;
            const extraSlash = (!originPlusPrefix.endsWith('/') && !input.value.startsWith('/')) ? '/' : '';

            if (!isLocalHost) {
                location.href = originPlusPrefix + extraSlash + input.value;
            } else {
                location.search = input.value;
            }

        });
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
        document.body.classList.add('discord');
        embedDiscordResource(url)
    }

    function embedDiscordExternal() {
        const exec = discordExternalUrlRegex.exec(location.href);
        if (!exec) {
            document.body.innerHTML += "<p style='color: red;'>Could not get external discord link from url!!</p>";
            return;
        }
        let url = exec.groups.resource;
        document.body.classList.add('discord-external');

        if (url.startsWith('https/')) {
            url = `https://${url.substring(6)}`;
        } else if (url.startsWith('http/')) {
            url = `https://${url.substring(5)}`
        }

        // const queryParts = exec.groups.query.split('/');
        // let query = decodeURIComponent(queryParts[queryParts.length - 2] ?? '');
        // if (!query.startsWith('?')) {
        //     query = `?${query}`;
        // }
        //
        // url += `${query}`;

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

    function embedRedgifs() {
        const exec = redgifsUrlRegex.exec(location.href);
        if (!exec) {
            document.body.innerHTML += "<p style='color: red;'>Could not get a resource id from the redgifs url!!</p>";
            return;
        }

        const resource = exec.groups.resource;
        const calculatedPadding = Math.floor((window.innerHeight / window.innerWidth * 100) + 0.5) - 2;
        const paddingBottom = Math.max(calculatedPadding, 10);

        document.body.classList.add('redgifs');
        document.body.style.overflowY = 'hidden';
        document.body.innerHTML += `
<div class="redgifs-container" style='position:relative; padding-bottom: ${paddingBottom}%'>
  <iframe src='https://redgifs.com/ifr/${resource}' frameBorder='0' scrolling='no' width='100%' height='100%' style='position:absolute; top:0; left:0;' allowFullScreen></iframe>
</div>`;

        document.body.querySelector('iframe').addEventListener('load', () => {
            setOffset();
        });

        function setOffset() {
            const iframe = document.body.querySelector('iframe');
            if (!iframe) {
                return;
            }

            iframe.style.left = '0';
            const bounds = iframe.getBoundingClientRect();
            if (bounds.x >= 0) {
                return;
            }

            let offset = -bounds.x;
            const halfWidth = Math.max((window.innerWidth - bounds.width) / 2, 0);
            offset += halfWidth;
            iframe.style.left = offset + "px";
        }

        window.addEventListener('resize', () => {
            const calculatedPadding = Math.floor((window.innerHeight / window.innerWidth * 100) + 0.5) - 2;
            const paddingBottom = Math.max(calculatedPadding, 10);
            document.body.querySelector('.redgifs-container').style.paddingBottom = `${paddingBottom}%`;
            setOffset();
        });
    }
}();
