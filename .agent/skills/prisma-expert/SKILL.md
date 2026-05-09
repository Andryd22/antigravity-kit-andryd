---
name: prisma-expert
description: Prisma ORM for type-safe database access. Schema design, migrations, relations, performance optimization, and serverless deployment patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Prisma Expert

> Type-safe ORM for PostgreSQL, MySQL, SQLite, and MongoDB. Schema-first, migration-safe.

## Schema Design

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@index([role])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published])
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

## Migration Safety

| Rule | Why |
|------|-----|
| `prisma migrate dev --create-only` first | Review SQL before applying |
| Never edit migration SQL manually | Prisma owns migration history |
| Test on staging DB copy first | Catch issues before production |
| Add nullable column → backfill → make required | Zero-downtime migration pattern |

## Query Performance

```typescript
// ❌ N+1: Separate queries for each user's posts
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } });
}

// ✅ Include: Single query with JOIN
const users = await prisma.user.findMany({
  include: { posts: true, profile: true },
});

// ✅ Select: Only needed fields
const users = await prisma.user.findMany({
  select: { id: true, email: true, name: true },
});
```

## Common Patterns

| Pattern | Code |
|---------|------|
| **Pagination** | `{ skip: 10, take: 10 }` |
| **Cascade delete** | `onDelete: Cascade` in schema |
| **Full-text search** | `where: { title: { contains: 'search' } }` |
| **Transaction** | `prisma.$transaction([...])` |
| **Raw query** | `prisma.$queryRaw\`SELECT * FROM ...\`` |

## Serverless/Edge

```typescript
// Use @prisma/client/edge for Vercel Edge / Cloudflare Workers
import { PrismaClient } from '@prisma/client/edge'
import { withAccelerate } from '@prisma/extension-accelerate'

const prisma = new PrismaClient().$extends(withAccelerate())
```

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `SELECT *` via no `select` | Explicit `select` or `include` |
| Skip indexes on FK columns | Add `@@index` on every FK |
| Use `env()` fallback values | Validate at startup, fail fast |
| Direct DB access from frontend | Server-side only via API routes |
| Ignore Prisma Studio for dev | Use `npx prisma studio` to inspect data |

## Checklist

- [ ] Schema uses appropriate types and relations
- [ ] Every foreign key has an index
- [ ] Migrations tested on staging first
- [ ] Queries use `select` or `include` explicitly
- [ ] Transactions used for multi-step mutations
- [ ] Connection pooling configured for serverless
