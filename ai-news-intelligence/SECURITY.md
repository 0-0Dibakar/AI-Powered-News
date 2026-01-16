"""Security best practices and hardening guide"""

# SECURITY CHECKLIST FOR PRODUCTION

## 1. Environment Variables
   ✓ Never commit .env files
   ✓ Use strong SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
   ✓ Rotate API keys regularly
   ✓ Use AWS Secrets Manager, Azure Key Vault, or similar

## 2. Database Security
   ✓ Enable PostgreSQL SSL connections
   ✓ Use strong passwords (20+ characters)
   ✓ Implement database-level encryption
   ✓ Regular backups to secure storage
   ✓ Restrict database access to backend only
   ✓ Enable audit logging

## 3. API Security
   ✓ HTTPS/TLS everywhere
   ✓ API key rotation
   ✓ Rate limiting enabled
   ✓ CORS properly configured
   ✓ Request size limits enforced
   ✓ JWT token expiration set to short duration

## 4. Authentication & Authorization
   ✓ Hash all passwords with bcrypt
   ✓ Implement multi-factor authentication (MFA)
   ✓ Session timeout after 30 minutes
   ✓ Role-based access control (RBAC)
   ✓ Audit user actions

## 5. Data Protection
   ✓ Encrypt sensitive data at rest
   ✓ Encrypt data in transit (TLS 1.3+)
   ✓ PII data handling compliant with GDPR/CCPA
   ✓ Implement data retention policies
   ✓ Secure deletion of archived data

## 6. Infrastructure Security
   ✓ Run containers with non-root user
   ✓ Use security groups/network policies
   ✓ Implement DDoS protection (CloudFlare, AWS Shield)
   ✓ Web Application Firewall (WAF) enabled
   ✓ Regular security audits and penetration testing

## 7. Logging & Monitoring
   ✓ Centralized logging (ELK, Datadog, etc.)
   ✓ No sensitive data in logs
   ✓ Monitor for suspicious activity
   ✓ Alert on security events
   ✓ Retain logs for compliance

## 8. Dependencies
   ✓ Regular security updates
   ✓ Vulnerability scanning (Snyk, Dependabot)
   ✓ Use pinned versions in requirements.txt
   ✓ Regular dependency audits

## 9. Code Security
   ✓ Code review process
   ✓ Static code analysis (SonarQube, Bandit)
   ✓ No hardcoded secrets
   ✓ Parameterized queries (SQL injection prevention)
   ✓ Input validation on all endpoints

## 10. Incident Response
   ✓ Incident response plan
   ✓ Regular backups tested
   ✓ Disaster recovery procedures
   ✓ 24/7 monitoring and alerting
   ✓ Incident post-mortems

---

## Example: Secure Configuration

### Backend Configuration

```python
# app/core/config.py - Production settings

from pydantic_settings import BaseSettings
import os

class ProductionSettings(BaseSettings):
    # HTTPS only
    SECURE_PROXY_HEADER: tuple = ("HTTP_X_FORWARDED_PROTO", "https")
    
    # Security headers
    SECURE_SSL_REDIRECT: bool = True
    SECURE_HSTS_SECONDS: int = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    SECURE_HSTS_PRELOAD: bool = True
    
    # Session security
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Strict"
    
    # CSRF protection
    CSRF_ENABLED: bool = True
    CSRF_TRUSTED_ORIGINS: list = ["https://yourdomain.com"]
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

```

### Nginx Security Headers

```nginx
# /etc/nginx/conf.d/security.conf

# HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL/TLS
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
    
    # Proxy to backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $host;
    }
}
```

### Docker Security

```dockerfile
# Use specific version tags, not 'latest'
FROM python:3.11-slim

# Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/api/health

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

## Regular Security Tasks

### Daily
- Monitor logs for suspicious activity
- Check rate limiting metrics
- Review error reports

### Weekly
- Review access logs
- Verify backups completed
- Check dependency updates

### Monthly
- Rotate API keys
- Review user access
- Update security policies

### Quarterly
- Penetration testing
- Security audit
- Review compliance

---

## Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [FastAPI Security](https://fastapi.tiangolo.com/advanced/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-syntax.html)
- [Redis Security](https://redis.io/docs/management/security/)

