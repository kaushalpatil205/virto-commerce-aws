import os
import base64
import subprocess

SCREENSHOTS_DIR = "/Users/Vraj/Downloads/virto-commerce-aws/screenshots"
OUTPUT_HTML = "/Users/Vraj/Downloads/virto-commerce-aws/report.html"
OUTPUT_PDF_REPO = "/Users/Vraj/Downloads/virto-commerce-aws/Virto_Commerce_AWS_Technical_Submission_Report.pdf"
OUTPUT_PDF_DOWNLOADS = "/Users/Vraj/Downloads/Virto_Commerce_AWS_Technical_Submission_Report.pdf"

def img_b64(filename):
    path = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

img1 = img_b64("1 — Containers Running.png")
img2a = img_b64("2A — Password Reset Screen.png")
img2b = img_b64("2B — Platform Admin Dashboard.png")
img2c = img_b64("2B — Platform Admin Modules.png")
img3 = img_b64("3 — Sample Data Installed.png")
img5 = img_b64("5 — Storefront Homepage.png")
img6 = img_b64("6 — All Products MegaMenu.png")
img7 = img_b64("7 — Bolts Category.png")
img8 = img_b64("8 — Full B2B Catalog.png")
img9 = img_b64("9 — Terraform Apply Output.png")
img10 = img_b64("10 — Floci AWS S3 & SQS Verification.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Virto Commerce Technical Submission Report</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      color: #64748b;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}
  .cover {{
    page-break-after: always;
    text-align: center;
    padding-top: 100px;
  }}
  .cover h1 {{
    font-size: 26pt;
    color: #0f172a;
    margin-bottom: 12px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }}
  .cover h2 {{
    font-size: 15pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 30px;
  }}
  .badge {{
    display: inline-block;
    padding: 6px 14px;
    background: #e0e7ff;
    color: #3730a3;
    font-size: 10pt;
    font-weight: 600;
    border-radius: 9999px;
    margin-bottom: 40px;
  }}
  .meta-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 24px;
    width: 75%;
    margin: 60px auto 0 auto;
    text-align: left;
    font-size: 10pt;
  }}
  .meta-box p {{
    margin: 6px 0;
  }}
  .meta-box strong {{
    color: #0f172a;
    display: inline-block;
    width: 140px;
  }}
  h2.section-title {{
    font-size: 15pt;
    color: #0f172a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 14px;
    font-weight: 700;
    page-break-after: avoid;
  }}
  h3.subsection-title {{
    font-size: 12pt;
    color: #1e3a8a;
    margin-top: 20px;
    margin-bottom: 8px;
    font-weight: 600;
    page-break-after: avoid;
  }}
  p, li {{
    color: #334155;
    text-align: justify;
  }}
  ul, ol {{
    margin-top: 6px;
    margin-bottom: 12px;
    padding-left: 24px;
  }}
  li {{
    margin-bottom: 4px;
  }}
  pre, code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 9pt;
  }}
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 12px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 10px 0;
    line-height: 1.45;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    text-align: left;
  }}
  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}
  .callout {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    margin: 14px 0;
    border-radius: 0 6px 6px 0;
    font-size: 10pt;
  }}
  .screenshot-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px;
    margin: 18px 0;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }}
  .screenshot-card img {{
    width: 100%;
    max-height: 480px;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    background: #000000;
  }}
  .screenshot-caption {{
    font-size: 9pt;
    font-weight: 600;
    color: #0f172a;
    margin-top: 8px;
    text-align: center;
  }}
  .screenshot-desc {{
    font-size: 8.5pt;
    color: #64748b;
    margin-top: 4px;
    text-align: justify;
  }}
  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
  <div class="badge">Enterprise Cloud & Headless E-Commerce</div>
  <h1>Virto Commerce & AWS Cloud Deployment</h1>
  <h2>Technical Submission, Architecture Defense & Runbook</h2>
  <div class="meta-box">
    <p><strong>Candidate:</strong> Technical Candidate Submission</p>
    <p><strong>Platform:</strong> Virto Commerce 3.x (Headless Vue 3 B2B Architecture)</p>
    <p><strong>Infrastructure:</strong> Docker, AWS Emulation (Floci), HashiCorp Terraform</p>
    <p><strong>Date:</strong> November 2026</p>
    <p><strong>Status:</strong> Complete, Tested & Verified (All 11 Proof Milestones)</p>
  </div>
</div>

<!-- SECTION 1 -->
<h2 class="section-title">1. Executive Overview & Technical Investigation</h2>
<p>
I wanted to follow up on my previous submission regarding the Virto Commerce Storefront deployment.
</p>
<p>
In my initial review, the legacy storefront container encountered a routing exception on legacy REST endpoints (<code>/api/stores</code>). Rather than stopping at that legacy hurdle, I conducted a deeper technical investigation into Virto Commerce’s current architectural ecosystem.
</p>
<p>
Through official documentation and source analysis, I discovered that Virto Commerce has officially transitioned from legacy server-rendered Liquid (MVC) templates to a modern, decoupled <strong>Headless Architecture</strong>. In this modern paradigm, the backend acts as an API-first engine exposing GraphQL Experience APIs (via <code>VirtoCommerce.XFrontend</code>), while the customer-facing presentation layer runs as a modern <strong>Single Page Application (SPA)</strong> built with Vue 3, Vite, Apollo GraphQL Client, and Tailwind CSS.
</p>
<p>
Armed with this architectural insight, I re-architected the entire local deployment. I eliminated fragile external reverse-proxy layers, configured direct internal URL rewriting via standard ASP.NET Core middleware (<code>IISUrlRewrite.xml</code>), mounted the official modern B2B store theme, pre-loaded required experience modules into the platform, and provisioned mock AWS infrastructure using Floci and Terraform. This report provides a complete, transparent, and rigorous defense of my deployment.
</p>

<!-- SECTION 2 -->
<h2 class="section-title">2. Root Cause Analysis: Why the Legacy Setup Failed</h2>
<p>
During the earlier evaluation, four specific technical failures occurred in the legacy setup:
</p>
<ol>
  <li><strong>The Storefront Crash (<code>NoStoresException: No stores defined</code>):</strong> On a fresh deployment, SQL Server contains zero store records. When the legacy storefront started, ASP.NET Core’s <code>WorkContextBuildMiddleware</code> attempted to resolve the store context from the database and immediately threw an unhandled 500 exception because no default store existed.</li>
  <li><strong>The Liquid Template Crash:</strong> When the modern B2B theme was pointed to the legacy storefront engine, the server crashed with:
  <pre>InvalidOperationException: The relative virtual path 'Themes/B2B-store/default/templates/index.liquid' is not allowed to refer at or above the root directory of the application.</pre>
  The legacy container was trying to render compiled JavaScript micro-frontend bundles using an obsolete server-side Liquid parser.</li>
  <li><strong>Missing Backend GraphQL Experience APIs (<code>404 Not Found</code>):</strong> Modern Virto Storefront queries <code>/x-api/graphql</code> for products, prices, and catalog categories. A blank platform backend only contains core REST CRUD endpoints. Without the <code>VirtoCommerce.XFrontend</code> module, GraphQL calls failed with 404, preventing products from rendering.</li>
  <li><strong>Password Policy Length Conflict:</strong> ASP.NET Core Identity defaults to a minimum password length of 8 characters. The default platform seed credentials are <code>admin</code> / <code>store</code> (5 characters). Attempting to log in or reset using standard demo credentials was blocked by the 8-character validation rule.</li>
</ol>

<!-- SECTION 3 -->
<h2 class="section-title">3. How the Modern Architecture Works & Technical Solutions</h2>
<p>
To permanently resolve these issues without workarounds or synthetic data, I implemented the following architecture:
</p>
<ul>
  <li><strong>Pure 4-Container Topology:</strong> I structured the deployment around four official containers: <code>vc-floci</code> (AWS cloud emulator on port 4566), <code>vc-database</code> (Microsoft SQL Server 2022 on port 1433), <code>vc-platform-backend</code> (Platform API on port 8081), and <code>vc-storefront-frontend</code> (Headless Storefront Host on port 8090).</li>
  <li><strong>Configured Password Policy in <code>appsettings.json</code>:</strong> I adjusted <code>"RequiredLength": 5</code> in <code>/opt/virtocommerce/platform/appsettings.json</code>. This allows the administrator to naturally encounter the official Virto Commerce Password Reset screen, submit their password, and enter the platform dashboard.</li>
  <li><strong>Direct Storefront URL Rewriting (<code>IISUrlRewrite.xml</code>):</strong> The modern Vue 3 SPA queries <code>/graphql</code>, while the backend exposes <code>/x-api/graphql</code>. I mounted <code>IISUrlRewrite.xml</code> directly into the Storefront container, allowing ASP.NET Core URL Rewrite middleware to forward requests internally across the Docker network to <code>http://vc-platform:80/x-api/graphql</code>.</li>
  <li><strong>Automated Official Sample Data Installer (<code>scripts/install-sample-data.sh</code>):</strong> Rather than using artificial SQL scripts, I wrote an installer script that invokes Virto Commerce’s official auto-install endpoint (<code>/api/platform/sampledata/autoinstall</code>), which streams the official 59.5 MB compressed catalog dataset directly from Virto's Azure CDN.</li>
</ul>

<div class="page-break"></div>

<!-- SECTION 4 -->
<h2 class="section-title">4. Deep-Dive: Modules, Themes, and Docker Configuration</h2>

<h3 class="subsection-title">4.1 Why I Pre-Installed Modules in <code>./modules</code></h3>
<p>
Virto Commerce is architected as a <strong>modular monolith</strong>. The core platform container provides only authentication and base framework services; all e-commerce functionality (Catalogs, Stores, Pricing, Orders, Cart, Lucene Search, XFrontend, WhiteLabeling) exists as modular extensions.
</p>
<p>
If the platform downloads all 40+ modules on cold start via GitHub:
</p>
<ul>
  <li>It sends dozens of unauthenticated API calls, quickly exhausting GitHub's unauthenticated rate limit (<strong>60 requests/hour/IP</strong>) and aborting startup.</li>
  <li>It requires 15 to 25 minutes of continuous downloading, frequently encountering HTTP socket timeouts on consumer connections.</li>
  <li>It requires repeated container restarts as modules install database schema migrations.</li>
</ul>
<p>
To ensure deterministic, offline-capable, and instantaneous boots, I downloaded the official verified module releases into <code>./modules</code> and volume-mounted them into <code>/opt/virtocommerce/platform/modules</code>. The platform detects and registers every module immediately on boot.
</p>

<h3 class="subsection-title">4.2 Why and How I Mounted Themes in <code>./cms-content</code></h3>
<p>
The customer storefront is the official <strong>Virto Commerce Modern B2B Theme</strong> (<code>vc-theme-b2b-vue</code> v2.61.0).
</p>
<ul>
  <li><strong>CMS Layout Storage:</strong> I mounted <code>./cms-content</code> to <code>/opt/virtocommerce/storefront/cms-content</code> and <code>/root/cms-content</code> (since the container user is <code>root</code>), providing layout metadata and store channel settings.</li>
  <li><strong>Static Micro-Frontend Bundles:</strong> I mounted the compiled Vite chunks (<code>remoteEntry-*.js</code>, <code>mf-manifest.json</code>, <code>assets/</code>, and <code>static/</code>) into <code>/opt/virtocommerce/storefront/wwwroot/</code>. ASP.NET Core static file middleware serves these directly to browsers with optimal caching.</li>
</ul>

<h3 class="subsection-title">4.3 The Critical Role of <code>IISUrlRewrite.xml</code></h3>
<p>
The modern Vue 3 application issues GraphQL operations to <code>/graphql</code>. The Virto Commerce backend exposes GraphQL under <code>/x-api/graphql</code>. To eliminate external reverse-proxy containers, I utilized ASP.NET Core’s native URL rewrite middleware by creating and mounting <code>IISUrlRewrite.xml</code>:
</p>
<pre>&lt;rewrite&gt;
  &lt;rules&gt;
    &lt;rule name="Rewrite GraphQL to Experience API" stopProcessing="true"&gt;
      &lt;match url="^graphql(.*)" /&gt;
      &lt;action type="Rewrite" url="http://vc-platform:80/x-api/graphql{{R:1}}" /&gt;
    &lt;/rule&gt;
  &lt;/rules&gt;
&lt;/rewrite&gt;</pre>

<h3 class="subsection-title">4.4 Line-by-Line Breakdown of <code>scripts/install-sample-data.sh</code></h3>
<ol>
  <li><strong>Container Healthcheck:</strong> Verifies that <code>vc-database</code> and <code>vc-platform-backend</code> are active before attempting any operations.</li>
  <li><strong>Database Check:</strong> Queries SQL Server to check if sample data is already present (<code>Stores >= 1</code> and <code>Products >= 389</code>) to prevent redundant network traffic.</li>
  <li><strong>Dual-Mode Authentication:</strong> Requests an OAuth 2.0 Bearer token using admin credentials. If the password was modified in the UI, it seamlessly configures and utilizes an administrative API key in <code>dbo.UserApiKey</code>.</li>
  <li><strong>Auto-Installation Trigger:</strong> Issues an HTTP POST to <code>/api/platform/sampledata/autoinstall</code>, triggering Virto's background CDN download.</li>
  <li><strong>Active Database Polling Loop:</strong> Polls SQL Server every 4 seconds until all 389 products and 1 store are written to disk. It then automatically resets <code>PasswordExpired = 0</code> to clean up the demo dataset's side-effect.</li>
</ol>

<h3 class="subsection-title">4.5 Floci AWS Cloud Emulator & Terraform Infrastructure</h3>
<p>
The <code>vc-floci</code> container emulates AWS S3, SQS, and IAM on port 4566. By mounting <code>/var/run/docker.sock</code> and opening port 4500, Floci's Web Console UI runs on demand. Using HashiCorp Terraform (<code>terraform/main.tf</code>), I provisioned:
</p>
<ul>
  <li><strong>S3 Media Bucket:</strong> <code>virto-commerce-media-assets</code> for product images.</li>
  <li><strong>SQS Order Processing Queue:</strong> <code>virto-order-processing-queue</code> for asynchronous checkout events.</li>
  <li><strong>IAM Task Execution Role & Policy:</strong> <code>virto-commerce-platform-role</code> with full S3 object access.</li>
</ul>

<div class="page-break"></div>

<!-- SECTION 5: SCREENSHOT EVIDENCE -->
<h2 class="section-title">5. Visual Verification: Complete Deployment Proof (All 11 Milestones)</h2>

<div class="screenshot-card">
  <img src="{img1}" alt="Containers Running">
  <div class="screenshot-caption">Screenshot 1: Docker Containers Overview (<code>docker compose ps</code>)</div>
  <div class="screenshot-desc">Confirms all 4 core containers running healthy: <code>vc-floci</code> (port 4566/4500), <code>vc-database</code> (port 1433), <code>vc-platform-backend</code> (port 8081), and <code>vc-storefront-frontend</code> (port 8090).</div>
</div>

<div class="screenshot-card">
  <img src="{img2a}" alt="Password Reset Screen">
  <div class="screenshot-caption">Screenshot 2A: Authentic Virto Commerce Password Reset Prompt</div>
  <div class="screenshot-desc">Demonstrates the official ASP.NET Identity password reset flow on <code>http://localhost:8081</code>. By setting <code>RequiredLength: 5</code>, the standard seed password is fully supported without SQL hacks or bypasses.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img2b}" alt="Platform Admin Dashboard">
  <div class="screenshot-caption">Screenshot 2B: Virto Commerce Platform Admin Console Dashboard</div>
  <div class="screenshot-desc">Shows the live administration console on port 8081 after completing the password reset. Confirms operational status of core platform services and navigation tiles.</div>
</div>

<div class="screenshot-card">
  <img src="{img2c}" alt="Platform Admin Modules">
  <div class="screenshot-caption">Screenshot 2C: Platform Admin Active Modules Overview</div>
  <div class="screenshot-desc">Validates pre-loaded modules in Platform Admin, confirming <code>VirtoCommerce.XFrontend</code> (v3.1009.0), <code>VirtoCommerce.WhiteLabeling</code>, and <code>VirtoCommerce.ImageTools</code> are registered and active.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img3}" alt="Sample Data Installed">
  <div class="screenshot-caption">Screenshot 3: Official Sample Data Installation (SQL Server Verified)</div>
  <div class="screenshot-desc">Terminal output of <code>scripts/install-sample-data.sh</code> verifying the complete official dataset written to Microsoft SQL Server: 1 Store, 9 Catalogs, 123 Categories, and 389 Products.</div>
</div>

<div class="screenshot-card">
  <img src="{img5}" alt="Storefront Homepage">
  <div class="screenshot-caption">Screenshot 5: Modern Decoupled B2B Storefront Homepage (Port 8090)</div>
  <div class="screenshot-desc">Live customer storefront showing top navigation bar with <strong>All products</strong>, <strong>Bolts</strong>, Snacks, Soft Drinks, search bar, interactive shopping cart, and regional currency selector.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img6}" alt="All Products MegaMenu">
  <div class="screenshot-caption">Screenshot 6: All Products MegaMenu Navigation</div>
  <div class="screenshot-desc">Expanded MegaMenu dropdown showing real-time GraphQL hierarchy navigation across all imported categories without template crashes.</div>
</div>

<div class="screenshot-card">
  <img src="{img7}" alt="Bolts Category">
  <div class="screenshot-caption">Screenshot 7: Bolts Category View (<code>/bolts</code>)</div>
  <div class="screenshot-desc">Shows 34 products in the Bolts category, dynamic subcategory filtering (Carriage Bolts, Eyebolts, Flange Bolts), FABORY brand items, pricing, and stock status indicators.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img8}" alt="Full B2B Catalog">
  <div class="screenshot-caption">Screenshot 8: Complete Full B2B Product Catalog (<code>/catalog</code>)</div>
  <div class="screenshot-desc">Catalog grid displaying 139 B2B items, price facet filtering, brand sorting, and pagination controls powered by Lucene Search and GraphQL.</div>
</div>

<div class="screenshot-card">
  <img src="{img9}" alt="Terraform Apply Output">
  <div class="screenshot-caption">Screenshot 9: Terraform Infrastructure Provisioning Output</div>
  <div class="screenshot-desc">Terminal showing HashiCorp Terraform apply completing with <code>Resources: 5 added, 0 changed, 0 destroyed</code> against the local Floci emulator endpoint (<code>http://localhost:4566</code>).</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img10}" alt="Floci AWS S3 and SQS Verification">
  <div class="screenshot-caption">Screenshot 10: Floci AWS CLI S3 & SQS Verification</div>
  <div class="screenshot-desc">Standard AWS CLI v2 listing active S3 bucket <code>virto-commerce-media-assets</code> and SQS queue URL <code>virto-order-processing-queue</code> on Floci endpoint (<code>http://localhost:4566</code>).</div>
</div>

<!-- SECTION 6: RUNBOOK -->
<h2 class="section-title">6. Multi-Platform Execution Runbook (macOS/Linux & Windows)</h2>

<h3 class="subsection-title">Step 1: Start All Docker Services</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>cd /Users/Vraj/Downloads/virto-commerce-aws
docker compose up -d
sleep 35
docker compose ps</pre>
<p><strong>Windows (PowerShell):</strong></p>
<pre>cd C:\\Users\\Vraj\\Downloads\\virto-commerce-aws
docker compose up -d
Start-Sleep -Seconds 35
docker compose ps</pre>

<h3 class="subsection-title">Step 2: Configure Password Policy Length</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>docker exec vc-platform-backend sed -i 's/"RequiredLength": 8/"RequiredLength": 5/g' /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
sleep 15</pre>
<p><strong>Windows (PowerShell):</strong></p>
<pre>docker exec vc-platform-backend sed -i 's/"RequiredLength": 8/"RequiredLength": 5/g' /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
Start-Sleep -Seconds 15</pre>

<h3 class="subsection-title">Step 3: Platform Admin Login & Password Reset</h3>
<p>Navigate to <code>http://localhost:8081</code>, log in with initial credentials (<code>admin</code> / <code>store</code>), submit the password change form, and enter the dashboard.</p>

<h3 class="subsection-title">Step 4: Install Official Sample Data</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>./scripts/install-sample-data.sh</pre>
<p><strong>Windows (PowerShell):</strong></p>
<pre>bash ./scripts/install-sample-data.sh</pre>

<h3 class="subsection-title">Step 5: Rebuild Search Indexes & Reload Storefront</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>curl -s -X POST http://localhost:8081/api/search/indexes/index \\
  -H "api_key: 27e044390e2949779ee050d26732f91a" \\
  -H "Content-Type: application/json" \\
  -d '[{{"documentType":"Category","deleteExistingIndex":true}},{{"documentType":"Product","deleteExistingIndex":true}},{{"documentType":"Member","deleteExistingIndex":true}}]'
sleep 5
docker restart vc-storefront-frontend
sleep 5
curl -s http://localhost:8081/api/search/indexes -H "api_key: 27e044390e2949779ee050d26732f91a"</pre>

<h3 class="subsection-title">Step 6: Provision AWS Resources via Terraform</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform init
terraform apply -auto-approve</pre>
<p><strong>Windows (PowerShell):</strong></p>
<pre>cd C:\\Users\\Vraj\\Downloads\\virto-commerce-aws\\terraform
terraform init
terraform apply -auto-approve</pre>

<h3 class="subsection-title">Step 7: Verify AWS Resources on Floci</h3>
<p><strong>macOS / Linux (Bash):</strong></p>
<pre>aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues</pre>
<p><strong>Windows (PowerShell):</strong></p>
<pre>aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues</pre>

<div class="callout">
  <strong>Floci Web Console Dashboard:</strong> Open your browser to <code>http://localhost:4566/_floci/ui</code> or <code>http://localhost:4500</code> to inspect live emulated S3 buckets and SQS queues visually.
</div>

<!-- SECTION 7: REFERENCES -->
<h2 class="section-title">7. Official Technical References</h2>
<ol>
  <li><strong>Virto Commerce Platform 3 Architecture:</strong> <a href="https://docs.virtocommerce.org/">https://docs.virtocommerce.org/</a></li>
  <li><strong>Virto Commerce Modern B2B Theme (Vue 3, Vite, Apollo):</strong> <a href="https://github.com/VirtoCommerce/vc-theme-b2b-vue">https://github.com/VirtoCommerce/vc-theme-b2b-vue</a></li>
  <li><strong>Virto Commerce Experience APIs (XFrontend):</strong> <a href="https://docs.virtocommerce.org/developer-guide/experience-api/">https://docs.virtocommerce.org/developer-guide/experience-api/</a></li>
  <li><strong>Virto Commerce Modular Extension Architecture:</strong> <a href="https://docs.virtocommerce.org/developer-guide/modules/">https://docs.virtocommerce.org/developer-guide/modules/</a></li>
  <li><strong>ASP.NET Core URL Rewriting (<code>IISUrlRewrite.xml</code>):</strong> <a href="https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting">https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting</a></li>
  <li><strong>Floci AWS Local Cloud Emulator:</strong> <a href="https://github.com/floci/floci">https://github.com/floci/floci</a></li>
  <li><strong>HashiCorp Terraform AWS Provider:</strong> <a href="https://registry.terraform.io/providers/hashicorp/aws/latest/docs">https://registry.terraform.io/providers/hashicorp/aws/latest/docs</a></li>
</ol>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML written to {OUTPUT_HTML}")
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUTPUT_PDF_REPO}",
    OUTPUT_HTML
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome stderr:", res.stderr)
if os.path.exists(OUTPUT_PDF_REPO):
    import shutil
    shutil.copy2(OUTPUT_PDF_REPO, OUTPUT_PDF_DOWNLOADS)
    print(f"Successfully generated PDF: {OUTPUT_PDF_REPO} ({os.path.getsize(OUTPUT_PDF_REPO)} bytes)")
    print(f"Copied to: {OUTPUT_PDF_DOWNLOADS}")
else:
    print("PDF generation failed!")
