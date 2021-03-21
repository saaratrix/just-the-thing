!function() {
    const isTenorRegex = /tenor\.com/;
    const tenorIdRegex = /\d+$/;

    window.addEventListener('load', () => {
        const isTenor = isTenorRegex.test(location.href);

        if (isTenor) {
            embedTenor();
        }


    });

    function embedTenor() {
        const regexResult = location.href.match(tenorIdRegex);
        const id = regexResult[0];

        if (!id) {
            document.body.innerHTML += "<p style='color: red;'>Could not get an id from the url!!</p>";
            return;
        }

        document.body.innerHTML += `<iframe allowtransparency="true" allowfullscreen="true" scrolling="no" style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://tenor.com/embed/${id}?canonicalurl=" frameborder="0"></iframe>`
    }
}();
