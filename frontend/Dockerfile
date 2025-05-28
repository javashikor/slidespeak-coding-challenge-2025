FROM oven/bun:1.1

WORKDIR /app

COPY . .

RUN bun install
# If your app has a build step (e.g. Bun + React), uncomment this:
# RUN bun run build

EXPOSE 3000

CMD ["bun", "run", "dev"]
