let cachedAuth = null;
let cachedAt = 0;

// Get (and cache) Backblaze account authorization
async function getB2Auth(env) {
    const now = Date.now();
    if (cachedAuth && now - cachedAt < 22 * 60 * 60 * 1000) return cachedAuth;

    const res = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
        headers: {
            Authorization: "Basic " + btoa(`${env.B2_KEY_ID}:${env.B2_KEY}`)
        }
    });

    if (!res.ok) throw new Error("Failed to authorize B2 account");

    const data = await res.json();
    cachedAuth = data;
    cachedAt = now;
    return data;
}

// Generate signed download URL for a single file
async function getSignedUrl(env, fileName) {
    const auth = await getB2Auth(env);
    const apiUrl = `${auth.apiUrl}/b2api/v2/b2_get_download_authorization`;

    const res = await fetch(apiUrl, {
        method: "POST",
        headers: {
            Authorization: auth.authorizationToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            bucketId: env.BUCKET_ID,
            fileNamePrefix: fileName,
            validDurationInSeconds: 3600
        })
    });

    if (!res.ok) {
        const err = await res.text();
        throw new Error(`Failed to get signed URL: ${err}`);
    }

    const data = await res.json();
    return `${auth.downloadUrl}/file/${env.BUCKET_NAME}/${fileName}?Authorization=${data.authorizationToken}`;
}

export default {
    async fetch(request, env, ctx) {
        try {
            const url = new URL(request.url);
            const basePath = `file/${env.BUCKET_NAME}`;

            // Remove basePath prefix
            let filePath = url.pathname.startsWith("/") ? url.pathname.slice(1) : url.pathname;
            if (filePath.startsWith(basePath)) {
                filePath = filePath.slice(basePath.length);
            }
            filePath = filePath.startsWith("/") ? filePath.slice(1) : filePath; // remove leading slash if any

            const cache = caches.default;
            let response = await cache.match(request);
            if (response) return response;

            const signedUrl = await getSignedUrl(env, filePath);
            const b2Res = await fetch(signedUrl);

            if (!b2Res.ok) {
                return new Response(`Error fetching from Backblaze: ${b2Res.statusText}`, {
                    status: b2Res.status
                });
            }

            response = new Response(b2Res.body, b2Res);
            response.headers.set("Cache-Control", "public, max-age=31536000, immutable");

            ctx.waitUntil(cache.put(request, response.clone()));
            return response;

        } catch (err) {
            return new Response("Error: " + err.message, {
                status: 500
            });
        }
    }
};