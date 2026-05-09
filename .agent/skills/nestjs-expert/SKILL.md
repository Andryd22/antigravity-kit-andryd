---
name: nestjs-expert
description: NestJS enterprise-grade server-side framework. Modules, dependency injection, guards, interceptors, pipes, decorators, and microservices.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# NestJS Expert

> Enterprise-grade Node.js with NestJS. Modules, DI, decorators, and microservices.

## Core Principles

| Principle | Rule |
|-----------|------|
| **Modularity** | Every feature in its own module |
| **DI First** | Constructor injection, no service locators |
| **Decorators** | Use built-in decorators, create custom when needed |
| **DTOs + Validation** | class-validator + class-transformer on every input |

## Module Structure

```
src/
├── users/
│   ├── users.module.ts
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   └── entities/
│       └── user.entity.ts
├── auth/
│   ├── auth.module.ts
│   ├── auth.controller.ts
│   ├── auth.service.ts
│   ├── guards/
│   │   └── jwt-auth.guard.ts
│   └── strategies/
│       └── jwt.strategy.ts
└── common/
    ├── decorators/
    ├── filters/
    ├── interceptors/
    └── pipes/
```

## Guards, Interceptors, Pipes, Filters

| Concept | Purpose | Execution Order |
|---------|---------|-----------------|
| **Pipe** | Validate/transform input | 1st |
| **Guard** | AuthN/AuthZ check | 2nd |
| **Interceptor (pre)** | Transform/map request | 3rd |
| **Controller** | Handle request | 4th |
| **Interceptor (post)** | Transform response | 5th |
| **Exception Filter** | Catch errors | On exception |

## Dependency Injection

```typescript
// ❌ AVOID: Service locator pattern
constructor(private readonly moduleRef: ModuleRef) {
  this.service = moduleRef.get(UserService);
}

// ✅ USE: Constructor injection
constructor(
  private readonly userService: UserService,
  private readonly configService: ConfigService,
) {}
```

## Decorator Patterns

```typescript
// Custom decorator for current user
export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);

// Usage in controller
@Get('profile')
getProfile(@CurrentUser() user: User) {
  return this.userService.getProfile(user.id);
}
```

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Put all logic in controller | Controller delegates to service |
| Use `any` in DTOs | Strict types with class-validator |
| Import modules with `require()` | Use DI: add to module imports/providers |
| One giant module | Feature modules per domain |
| Skip DTO validation pipes | `app.useGlobalPipes(new ValidationPipe())` |

## Checklist

- [ ] Feature modules per domain
- [ ] DTOs with class-validator decorators
- [ ] Global validation pipe configured
- [ ] Guards for auth endpoints
- [ ] Exception filters for consistent error responses
- [ ] Swagger/OpenAPI decorators on controllers
