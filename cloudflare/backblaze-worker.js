let cachedAuth = null
let cachedAt = 0

async function getB2Auth(env) {
    const now = Date.now()
    // If cached token is less than 22h old, reuse it
    if (cachedAuth && (now - cachedAt < 22 * 60 * 60 * 1000)) {
        return cachedAuth
    }

    // Otherwise, reauthorize
    const res = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
        headers: {
            Authorization: "Basic " + btoa(env.B2_KEY_ID + ":" + env.B2_KEY)
        }
    })
    const data = await res.json()

    cachedAuth = data
    cachedAt = now
    return cachedAuth
}

export default {
    async fetch(request, env) {
    // # TODO fix some day since even unregistered users can access app
//        const cookie = request.headers.get("Cookie") || ""
//        if (!cookie.includes("sessionId")) {
//            return new Response("Unauthorized", {
//                status: 401
//            })
//        }

        const {
            downloadUrl,
            authorizationToken
        } = await getB2Auth(env)


        const url = new URL(request.url)

        // Base path to strip
        const basePath = `file/${env.BUCKET_NAME}`;

        // Remove leading "/" if present
        let filePath = url.pathname.startsWith("/") ? url.pathname.slice(1) : url.pathname;

        // Remove the base path prefix
        if (filePath.startsWith(basePath)) {
            filePath = filePath.slice(basePath.length);
        }

        const b2Url = `${downloadUrl}/${basePath}/${filePath}`

        const b2Res = await fetch(b2Url, {
            headers: {
                Authorization: authorizationToken
            }
        })

        // Copy B2 headers dynamically
        const newHeaders = new Headers(b2Res.headers)
        newHeaders.set("Cache-Control", "public, max-age=31536000") // add CDN caching

        return new Response(b2Res.body, {
            headers: newHeaders,
            status: b2Res.status
        })
    }
}