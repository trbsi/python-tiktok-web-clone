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
        const pathParts = url.pathname.split("/") // split by "/"
        const fileName = pathParts[pathParts.length - 1] // get last segment
        const b2Url = `${downloadUrl}/file/${env.BUCKET_NAME}/${fileName}`

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