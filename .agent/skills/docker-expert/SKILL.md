---
name: docker-expert
description: Docker containerization and Docker Compose. Dockerfile optimization, multi-stage builds, security hardening, and production patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Docker Expert

> Containerization, Dockerfiles, Docker Compose, and production patterns.

## Dockerfile Best Practices

```dockerfile
# ✅ Multi-stage build
FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS build
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS production
WORKDIR /app
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=base /app/node_modules ./node_modules
COPY package*.json ./
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

## Layer Optimization

| Rule | Why |
|------|-----|
| `COPY package*.json` before `COPY .` | Cache npm install unless deps change |
| Combine `RUN` commands with `&&` | Fewer layers = smaller image |
| `--chown=node:node` on COPY | Non-root user from the start |
| `.dockerignore` `node_modules` | Don't copy host node_modules |

## Docker Compose

```yaml
version: "3.9"
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s

volumes:
  pgdata:
```

## Security Hardening

| Practice | Command / Setting |
|----------|-------------------|
| Run as non-root | `USER node` |
| No latest tag | `FROM node:22-alpine` not `:latest` |
| Scan for vulns | `docker scan <image>` |
| Read-only rootfs | `read_only: true` in compose |
| Drop capabilities | `cap_drop: [ALL]` |
| Limit resources | `deploy: resources: limits: { memory: 512M }` |

## Production Patterns

```dockerfile
# Health check with wget (Alpine)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# Use ARG for build-time vars
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `FROM node:latest` | Pin exact version `node:22-alpine` |
| `COPY . .` first | Copy `package.json` first (cache layer) |
| Run as root | `USER node` |
| `.env` file in image | inject via runtime or secrets |
| One giant layer | Multi-stage, minimal layers |
| No healthcheck | HEALTHCHECK on every service |

## Checklist

- [ ] Multi-stage build reduces final image size
- [ ] `.dockerignore` excludes `node_modules`, `.git`, `.env`
- [ ] Non-root user (`USER node`)
- [ ] Tags pinned (no `:latest`)
- [ ] HEALTHCHECK configured
- [ ] `depends_on` with `condition: service_healthy`
- [ ] Secrets via runtime injection, not in image
