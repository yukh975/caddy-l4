Name:    caddy-l4
Version: %%VERSION%%
Release: %%RELEASE%%

Summary: Layer 4 (TCP/UDP) routing app for Caddy
License: Apache-2.0
Group:   System/Servers
Url:     https://github.com/mholt/caddy-l4

# Pre-built binary produced by the CI pipeline.
# To build locally: install xcaddy, then run:
#   xcaddy build --with github.com/mholt/caddy-l4@v%%VERSION%% --output caddy
Source0: caddy
Source1: caddy-l4.service
Source2: Caddyfile.example

ExclusiveArch: x86_64 aarch64

BuildRequires: systemd-rpm-macros

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Conflicts: caddy

%description
caddy-l4 provides Layer 4 (TCP/UDP) routing for the Caddy web server.

Key features:
- TLS passthrough with SNI-based routing (no certificate needed)
- Protocol detection: HTTP, TLS, SSH, and more
- PROXY protocol support (v1 and v2)
- UDP proxying including QUIC/HTTP3
- Load balancing across multiple backends

%prep
# Binary is pre-built by the CI pipeline — nothing to unpack.

%build
# Nothing to compile.

%install
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/bin/caddy
install -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/caddy-l4.service
install -D -m 0644 %{SOURCE2} %{buildroot}/etc/caddy/Caddyfile.example

install -d %{buildroot}/var/lib/caddy
install -d %{buildroot}/var/log/caddy

%pre
getent group  caddy &>/dev/null || groupadd -r caddy
getent passwd caddy &>/dev/null || \
    useradd -r -g caddy -d /var/lib/caddy -s /sbin/nologin \
            -c "Caddy L4 service account" caddy

%post
%systemd_post caddy-l4.service

%preun
%systemd_preun caddy-l4.service

%postun
%systemd_postun_with_restart caddy-l4.service

%files
%doc README.md
%license LICENSE
/usr/bin/caddy
/usr/lib/systemd/system/caddy-l4.service
%dir /etc/caddy
%config(noreplace) /etc/caddy/Caddyfile.example
%dir %attr(0750,caddy,caddy) /var/lib/caddy
%dir %attr(0750,caddy,caddy) /var/log/caddy

%changelog
* %%DATE%% Packager <packager@example.com> %%VERSION%%-%%RELEASE%%
- Automated build
