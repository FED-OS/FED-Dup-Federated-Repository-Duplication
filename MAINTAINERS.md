# Fed-Dup Maintainers Guide

## 👤 Current Maintainers

### Lead Maintainer
- **Your Name** — [@yourusername](https://github.com/yourusername)
  - Project direction
  - Code reviews
  - Release management

## 🔧 Maintainer Responsibilities

### Code Review
- Review PRs within 48 hours
- Ensure tests pass and code coverage doesn't decrease
- Check for security issues
- Verify documentation updates

### Release Management
- Create release tags (`v1.0.0` format)
- Write release notes
- Publish to PyPI and Docker Hub (automated via `cd.yml`/`publish.yml`)
- Announce releases

### Community Management
- Triage issues
- Answer questions in discussions
- Label and organize issues/PRs
- Enforce Code of Conduct

### Documentation
- Keep README up to date
- Maintain examples
- Update CHANGELOG.md
- Ensure API documentation is complete

## 🚀 Release Process

1. Ensure all tests pass (`pytest tests/ -v`)
2. Update `CHANGELOG.md`
3. Bump version in `feddup/__init__.py`
4. Create PR for version bump
5. After merge, create tag `vX.Y.Z`
6. GitHub Actions handles publishing (CD + Release workflows)

## 🛡️ Security Response

### Security Vulnerability Handling
1. Create a private security advisory
2. Investigate and fix issue
3. Release patch version
4. Announce fix in security advisory

### Responsible Disclosure
- Security issues should be reported via GitHub Security Advisory
- Do not open public issues for security vulnerabilities
- See `SECURITY.md` for response timelines

## 📋 Merge Criteria

- ✅ All CI checks pass
- ✅ At least one maintainer approval
- ✅ Test coverage doesn't decrease
- ✅ Documentation updated
- ✅ No breaking changes without discussion

## 🔐 Access Control

### GitHub Permissions
- **Maintain**: Full repository access
- **Triage**: Issue/PR management
- **Write**: Push to branches, create releases

### PyPI Ownership
- Current maintainer is the only PyPI uploader
- Add maintainers via PyPI project settings

### Docker Hub Ownership
- Fed-Dup image under organization namespace
- Maintainers added as collaborators

## 📊 Monitoring

Track these metrics weekly:
- Active issues/PRs
- Response time
- Release adoption
- Test coverage percentage

## 💡 Best Practices

1. **Be welcoming** to new contributors
2. **Respond quickly** to questions
3. **Document decisions** in `docs/ADR.md`
4. **Keep dependencies minimal**
5. **Test before merging**
6. **Write clear commit messages**

---

**Thank you for maintaining Fed-Dup! 🛡️**
