def build_prompt(error: str, code_context: list, retrieved_docs: list, env_data: dict = None) -> str:
    sb_version_str = ""
    if env_data and env_data.get('spring_boot_version'):
        sb_version_str = f" for Spring Boot version {env_data.get('spring_boot_version')}"

    prompt = f"""
You are **SpringForge**, an expert Spring Boot runtime debugging assistant.

Your goal is to analyze a runtime error{sb_version_str} and return a **clear, concise, developer-friendly fix**
suitable for display inside an IDE popup.

<error_trace>
{error}
</error_trace>
"""

    if env_data:
        prompt += "\n<environment_summary>\n"
        if env_data.get('jdk_version'):
            prompt += f"JDK version: {env_data.get('jdk_version')}\n"
        if env_data.get('spring_boot_version'):
            prompt += f"Spring Boot version: {env_data.get('spring_boot_version')}\n"
        if env_data.get('build_file_name'):
            prompt += f"Build file: {env_data.get('build_file_name')}\n"
        driver_hint = _detect_database_driver(env_data.get('build_file_content', ''))
        if driver_hint:
            prompt += f"Detected database driver: {driver_hint}\n"
            print(f"Detected database driver: {driver_hint}")
        prompt += "</environment_summary>\n"

    if code_context:
        prompt += "\n<project_files>\n"
        for file in code_context:
            # Using .get() ensures it won't crash if a key is missing
            prompt += f"""<file path="{file.get('path', 'unknown')}" category="{file.get('category', 'unknown')}">
{file.get('content', '')}
</file>\n"""
        prompt += "</project_files>\n"

    if env_data and env_data.get('build_file_content'):
        build_name = env_data.get('build_file_name', 'pom.xml / build.gradle')
        prompt += f"""
<build_configuration name="{build_name}">
{env_data.get('build_file_content', '')}
</build_configuration>
"""

    prompt += "\n<retrieved_context>\n"
    if retrieved_docs:
        for doc in retrieved_docs:
            prompt += f"""<doc title="{doc.get('title', 'Unknown')}" url="{doc.get('url', '#')}" source="{doc.get('source', 'unknown')}">
{doc.get('content', '')}
</doc>\n"""
    else:
        prompt += "No external documentation retrieved.\n"
    prompt += "</retrieved_context>\n"

    prompt += """
──────────────────────────

Produce the response in the EXACT format below.

FORMAT (STRICT):

Error:
<one-line summary>

Root Cause:
<1–2 sentences>

Suggested Fix:
<short explanation>

```<language>
// minimal, valid corrected code (e.g., java, xml, properties, yaml)
```

References:
<ONLY list URLs from the RETRIEVED CONTEXT that directly helped you solve this bug.
If the retrieved context was irrelevant and you used your internal knowledge, output EXACTLY:
"- No relevant documentation found in the knowledge base. Solution generated from core Spring Boot principles.">

Notes:
<optional edge cases or alternatives (max 2 bullets)>

──────────────────────────
IMPORTANT RULES:

Be concise and precise.

Prefer Spring Boot best practices.

If code is shown, it MUST be valid and minimal.

Do NOT invent files, classes, or dependencies.

Do NOT repeat the stacktrace.

CRITICAL DEPENDENCY-AWARE RULE:

You MUST carefully analyze the provided <build_configuration>.

Infer the frameworks, libraries, and exact Spring Boot version already included.

Version Ecosystem: Ensure that any suggested imports, application properties, or dependencies strictly align with the major/minor version of Spring Boot detected in the build file (e.g., correct dependency namespaces, valid property keys for that specific era of Spring).

BOM Management: If a fix requires adjusting a Spring-managed dependency, prefer removing explicit version tags to let the Spring Boot Dependency Management (BOM) handle it, unless a specific version override is the exact solution to the bug.

Tailor your fix to the technologies that are already present. Do NOT assume default technologies.

Only recommend adding a new dependency if it is absolutely required to resolve the error. Ensure it does not conflict with declared dependencies.

CRITICAL DATABASE RULE (FOR DEMO STABILITY):
If the runtime error is related to a missing DataSource, database url, or connection:

First, check the <environment_summary> and <build_configuration>. If a specific driver exists (e.g., mysql-connector-j), provide the connection properties ONLY for that database.

If NO database driver is explicitly found, you MUST suggest adding the H2 in-memory database (com.h2database:h2) and its associated application properties.

NEVER suggest setting up external databases like PostgreSQL, MySQL, or MongoDB unless their specific driver is already present in the build file. Always default to an embedded H2 database for missing connection errors.

CRITICAL ANTI-HALLUCINATION RULE:

Do NOT invent or hallucinate URLs.

You may ONLY cite URLs explicitly provided in the <retrieved_context> block above.
"""

    return prompt


def _detect_database_driver(build_file_content: str) -> str:
    content = (build_file_content or "").lower()

    if "mysql-connector-j" in content or "mysql:mysql-connector" in content:
        return "mysql"
    if "mariadb" in content:
        return "mariadb"
    if "postgresql" in content:
        return "postgresql"
    if "mssql" in content or "sqlserver" in content:
        return "sql server"
    if "oracle" in content:
        return "oracle"

    return ""