# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in brawlstars-twitch, please **do not** open a public GitHub issue. Instead, please report it privately by:

1. Emailing the repository maintainer with details of the vulnerability
2. Including proof-of-concept code or steps to reproduce
3. Allowing reasonable time for a fix before public disclosure

We take all security reports seriously and will work to address confirmed vulnerabilities promptly.

## Security Considerations

### Twitch Credentials & API Keys

- **Store securely**: Never commit `.env` files, API keys, or client secrets to version control. Use `.gitignore` to exclude `.env`.
- **Environment variables**: Load all sensitive credentials (e.g., `APPLICATION_CLIENT_ID`, `APPLICATION_CLIENT_SECRET`) from environment variables, not hardcoded in source files.
- **Token rotation**: Regularly rotate Twitch OAuth tokens and client secrets, especially if credentials may have been exposed.
- **Access scope**: Request only the minimum Twitch OAuth scopes needed (e.g., `moderator:read:followers` for follow events). Avoid overly broad permissions.

### Production Deployment

- **HTTPS only**: Deploy with HTTPS in production. Configure a reverse proxy (nginx, Apache) or use a platform that enforces TLS.
- **CORS & origins**: Restrict Cross-Origin Resource Sharing (CORS) to trusted domains. Do not enable `*` CORS in production.
- **WebSocket security**: Twitch EventSub WebSockets should only connect over `wss://` (secure). Verify certificate validity.
- **Rate limiting**: Implement rate limiting on the `/follower_stream` SSE endpoint and other public routes to prevent abuse.
- **Authentication for admin routes**: If you add admin endpoints (e.g., to trigger demo followers or adjust settings), require authentication (API keys, OAuth, etc.).

### Data & Privacy

- **Follower data**: Treat follower usernames and metadata as sensitive. If logging or persisting follower events, do so securely and in compliance with applicable privacy laws.
- **Event logging**: Avoid logging full EventSub payloads to disk or third-party services without sanitization.
- **User consent**: Ensure your overlay and Twitch integration comply with Twitch's Terms of Service and your jurisdiction's privacy regulations.

### Local Development

- **Sandbox environment**: Use `DEMO_MODE = True` to test overlays without production Twitch credentials.
- **Local testing**: Run locally on `127.0.0.1` or a private network only. Do not expose to the public internet during development.
- **Credentials in dev**: Even in dev, store credentials in `.env` and load via environment variables, not hardcoded.

### Code & Dependencies

- **Dependencies**: Regularly update Python packages (Flask, requests, etc.) to patch security vulnerabilities. Use `pip install --upgrade <package>` and review release notes for breaking changes.
- **Input validation**: If you extend the overlay to accept user input (e.g., custom text, settings), validate and sanitize all inputs to prevent injection attacks (XSS, command injection, etc.).
- **JavaScript safety**: The frontend overlay code runs in the browser. Avoid `eval()` and unsafe DOM manipulation. Use `textContent` instead of `innerHTML` when displaying user-provided text.

### Queue & Scaling

- **In-memory queue**: The default `queue.Queue` is not persistent. If your stream process crashes, pending followers are lost. For reliability, migrate to Redis or RabbitMQ with persistence.
- **Redis/RabbitMQ security**: If using an external queue service, secure it with strong authentication, network isolation, and encryption in transit (TLS).

### EventSub & Webhooks

- **EventSub WebSocket**: The current implementation uses secure WebSocket connections. Ensure your network allows outbound connections to Twitch's EventSub servers.
- **EventSub verification**: Always verify EventSub event signatures if switching to webhook-based subscriptions. Twitch provides `x-hub-signature` headers; validate them to prevent forged events.

### Overlay Page Security

- **XSS prevention**: The overlay page (`templates/follower_rank.html`) should sanitize any dynamic content before rendering. If follower usernames are displayed, encode them to prevent HTML/JavaScript injection.
- **Same-site cookies**: If you add session cookies in the future, use `SameSite=Strict` or `SameSite=Lax` to mitigate CSRF attacks.
- **Content Security Policy (CSP)**: Consider adding a CSP header to restrict resource loading and inline scripts on the overlay page.

## Recommended Security Checklist for Production

- [ ] All credentials are stored in environment variables, not in source code
- [ ] `.env` and sensitive files are in `.gitignore`
- [ ] HTTPS / TLS is enabled and enforced
- [ ] CORS is restricted to trusted domains
- [ ] Rate limiting is configured on public endpoints
- [ ] Admin/control endpoints require authentication
- [ ] Dependencies are up-to-date and scanned for vulnerabilities
- [ ] Input validation and output encoding are in place
- [ ] WebSocket connections use secure `wss://` protocols
- [ ] EventSub events are verified (if using webhooks)
- [ ] Follower data is handled in compliance with privacy laws
- [ ] Monitoring and logging are in place (without exposing sensitive data)

## Security Updates

Stay informed of security best practices and Twitch API changes:

- Monitor [Twitch Developer Changelog](https://dev.twitch.tv/changelog)
- Subscribe to security advisories for dependencies (e.g., Flask, requests)
- Follow GitHub's security recommendations for this repository

## Third-Party Services

This project integrates with Twitch. Review Twitch's own security policies:

- [Twitch Security](https://www.twitch.tv/security)
- [Twitch EventSub Documentation](https://dev.twitch.tv/docs/eventsub)
- [Twitch OAuth Best Practices](https://dev.twitch.tv/docs/authentication)

## Questions or Concerns?

If you have security questions or concerns beyond vulnerability reporting, open a discussion or issue in this repository. We're happy to help clarify secure usage patterns.
