# SmoothSak

Static source for `smoothsak.com`. The complete website is in
`smoothsak.com/html/`; there is no application server, package installation, or
compilation step.

## Production deployment

Use the sibling [website-deploy](https://github.com/bousborne/website-deploy)
checkout on the H5. It publishes this repository's static files into the
`smoothsak-data` Docker volume, serves them with nginx, and uses HomeNet's Caddy
for public HTTPS.

```bash
cd /home/bousborne
git clone --branch master git@github.com:bousborne/SmoothSak.git
cd website-deploy
./run.sh
./check.sh
```

If the checkout already exists, update it with
`git -C /home/bousborne/SmoothSak pull --ff-only origin master` instead of cloning
again. See the deployment repository for the other required sibling checkouts.

Only `smoothsak.com/html/` should be published; never serve the repository root
or its `.git` directory. The existing navigation and product buttons are template
placeholders, not a storefront or checkout system.

## Local verification

Check that HTML/CSS references resolve to local assets and external
resources use HTTPS:

```bash
python3 tests/verify_static_site.py
```

Preview without installing dependencies:

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory smoothsak.com/html
```
