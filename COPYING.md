# Copying

## License

Fed-Dup is licensed under the **MIT License**, a permissive free-software
license. The full text of the license is in the [LICENSE](LICENSE) file and
is reproduced below for convenience.

### MIT License

```
MIT License

Copyright (c) 2025 Fed-Dup Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## What the MIT License Allows

The MIT License grants you the following rights, free of charge:

- ✅ **Use** — use Fed-Dup for any purpose, including commercial use.
- ✅ **Copy** — make and distribute copies of the software.
- ✅ **Modify** — change the code to suit your needs.
- ✅ **Merge** — incorporate Fed-Dup into your own projects.
- ✅ **Publish** — distribute the original or modified software.
- ✅ **Distribute** — share the software with others.
- ✅ **Sublicense** — grant licenses to others under the same terms.
- ✅ **Sell** — sell copies of the software (e.g., as part of a product).

---

## What You Must Do

The MIT License has only two conditions:

1. **Include the copyright notice** — the line `Copyright (c) 2025 Fed-Dup
   Contributors` must appear in all copies or substantial portions of the
   software.
2. **Include the permission notice** — the full permission paragraph
   (reproduced above) must accompany the copyright notice.

That is it. There is no requirement to share your modifications, attribute the
project in your UI, or pay any fees.

---

## What You Must NOT Do

- ❌ **Hold the authors liable** — the software is provided "as is", without
  warranty. The authors are not responsible for any damage or data loss
  caused by the software.
- ❌ **Remove the license text** — the copyright and permission notices must
  remain in all copies.

---

## The NOTICE File

The [NOTICE.md](NOTICE.md) file contains copyright information and
acknowledgements for Fed-Dup and its third-party dependencies. While not
strictly required by the MIT License, it is good practice and is included in
all distributions.

---

## Third-Party Dependencies

Fed-Dup depends on the following open-source projects, each with their own
license. These licenses are compatible with the MIT License:

| Dependency    | License     | Notes                              |
|---------------|-------------|------------------------------------|
| Python        | PSF License | Runtime language                   |
| Streamlit     | Apache 2.0  | Web UI framework                   |
| Git           | GPLv2       | Called as a subprocess (not linked)|
| pytest        | MIT         | Testing (dev only)                 |
| black         | MIT         | Formatting (dev only)              |
| flake8        | MIT         | Linting (dev only)                 |
| mypy          | MIT         | Type checking (dev only)           |
| bandit        | Apache 2.0  | Security linting (dev only)        |

> **Note on Git:** Git is licensed under GPLv2. Fed-Dup does not link to or
> distribute Git — it invokes the `git` binary as a subprocess. This is
> analogous to a shell script calling Git and does not create a derivative
> work under the GPL. The MIT License on Fed-Dup is not affected.

---

## Including Fed-Dup in Your Project

If you copy, fork, or embed Fed-Dup in your own project:

1. Keep the [LICENSE](LICENSE) file in your distribution.
2. Keep the [NOTICE.md](NOTICE.md) file (recommended).
3. Retain the copyright notice in source files.
4. You are free to change the project name, modify the code, and distribute
   under your own brand — just keep the license and copyright notice.

---

## Dual Licensing

Fed-Dup is **not** dual-licensed. The MIT License is the sole license for the
entire project. There is no commercial license and no need for one — the MIT
License already permits commercial use.

---

## Contact

Questions about licensing or copying? Open a
[GitHub Discussion](https://github.com/feddup/fed-dup/discussions) or refer to
the [MIT License text](https://opensource.org/license/mit) on the Open Source
Initiative website.
