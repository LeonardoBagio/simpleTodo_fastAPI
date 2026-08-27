# ---------- build stage ----------
FROM node:22-slim AS build

WORKDIR /app

# Install deps first for better layer caching. .npmrc carries legacy-peer-deps
# (vue-router 5 optional peers trip npm's resolver otherwise).
COPY package.json .npmrc ./
RUN npm install

# Build the Nuxt/Nitro output (self-hosted Google Fonts are fetched here).
COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM node:22-slim AS runtime

WORKDIR /app

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000

# Only the Nitro server output is needed at runtime.
COPY --from=build /app/.output ./.output

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
