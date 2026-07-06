from pathlib import Path

SKILLS_DIR = "skills"


def list_skills():

    try:

        skills = []

        for file in Path(
            SKILLS_DIR
        ).glob("*.md"):

            skills.append(
                file.stem
            )

        return {
            "skills": skills
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def load_skill(name):

    try:

        path = (
            Path(SKILLS_DIR)
            / f"{name}.md"
        )

        if not path.exists():

            return {
                "error":
                "Skill not found"
            }

        return {
            "content":
            path.read_text()
        }

    except Exception as e:

        return {
            "error": str(e)
        }


__all__ = [
    "list_skills",
    "load_skill"
]