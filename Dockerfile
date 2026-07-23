FROM node:24.18.0-alpine AS build
WORKDIR /workspace
COPY package.json package-lock.json ./
COPY packages ./packages
COPY tests ./tests
COPY tsconfig.json tsconfig.base.json ./
RUN npm ci && npm run build

FROM node:24.18.0-alpine
WORKDIR /app
COPY --from=build /workspace/package.json /workspace/package-lock.json ./
COPY --from=build /workspace/node_modules ./node_modules
COPY --from=build /workspace/packages ./packages
USER node
ENV APP_PORT=8084
EXPOSE 8084
CMD ["node", "packages/api/dist/main.js"]
