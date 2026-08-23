# Security vulnerability audits in ROS ESM

ROS ESM is maintained by the Ubuntu Robotics Team, in a close partnership with the
Ubuntu security team. Its security processes apply the same rigor that
secures millions of Ubuntu systems. This collaboration ensures timely
triage and patching of vulnerabilities, as quickly as 24 hours
for reported critical issues.
ROS packages benefit from Canonical's expertise in vulnerability disclosure
and non-disruptive updates, all aligned with Ubuntu LTS standards.
Delivered through Ubuntu Pro, ROS ESM offers unified, long-term security
and compliance for robotics deployments.

In addition to addressing reported security vulnerabilities, the Ubuntu Robotics
team proactively runs a dedicated security analysis pipeline for ROS packages.

## A close look at ROS ESM's ongoing security audits

The team leverages advanced static analysis using tools like
[Semgrep](https://semgrep.dev/), [Bandit](https://github.com/PyCQA/bandit), and
[Coverity](https://scan.coverity.com/) to detect memory safety vulnerabilities,
insecure APIs, logic errors, and other high-risk code patterns
in the ROS distributions it supports.
Identified issues undergo rigorous triage by engineers, with critical findings
validated through dynamic analysis and vulnerability proof-of-concept testing.
Fixes are then delivered through a **controlled, quality-focused release process**
that ensures both reliability and traceability.
Security fixes are tested and staged before being deployed to users,
and where appropriate, Canonical contributes them to upstream ROS repositories,
following a **responsible, coordinated disclosure**,
and ROS's own [Vulnerability Disclosure Policy](https://ros.org/reps/rep-2006.html).

This is backed by a **robust, purpose-built CI infrastructure**
that spans multiple stages of quality assurance.
The pipeline runs a sequence of automated checks, including unit tests,
ABI stability tests, reverse dependency testing,
integration tests with external packages, and full Debian packaging via [Bloom](https://github.com/ros-infrastructure/bloom).
The integration tests confirm that
**ROS ESM packages remain installable, compatible, and functional**
when used alongside other ROS packages. This helps prevent regressions
and ensures compatibility across supported platforms and architectures.

## Security issues detected and fixed

As a direct result of this proactive security work, several vulnerabilities
in the ROS ecosystem have been
**identified, responsibly disclosed, and patched on ROS ESM**. This includes
the publication and remediation of multiple High severity CVEs, such as:

- [CVE-2025-3753  - Code execution vulnerability in rosbag](https://nvd.nist.gov/vuln/detail/CVE-2025-3753)
- [CVE-2024-39289 - Code execution vulnerability in rosparam](https://nvd.nist.gov/vuln/detail/CVE-2024-39289)
- [CVE-2024-39780 - YAML deserialization vulnerability in dynparam](https://nvd.nist.gov/vuln/detail/CVE-2024-39780)
- [CVE-2024-39835 - Code injection vulnerability in roslaunch](https://nvd.nist.gov/vuln/detail/CVE-2024-39835)
- [CVE-2024-41148 - Code injection vulnerability in rostopic](https://nvd.nist.gov/vuln/detail/CVE-2024-41148)
- [CVE-2024-41921 - Code injection vulnerability in rostopic](https://nvd.nist.gov/vuln/detail/CVE-2024-41921)

These fixes demonstrate the value of continuous auditing,
as well as Canonical's commitment to raising the security baseline
for ROS-based systems in production.

If you're running ROS in production, it's important to know
whether a specific CVE has been patched in your environment.
To do this, check out {ref}`How to check if a CVE is fixed in your environment <how-to-guides-maintenance-check-cves>`.
