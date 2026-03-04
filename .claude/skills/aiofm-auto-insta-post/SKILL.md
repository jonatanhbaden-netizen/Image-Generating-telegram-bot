---
name: aiofm-auto-insta-post
description: Use when someone asks to create an Instagram post or swap a model in a scene image. Swaps the model in a provided scene image with a stored AI model image using Fal.ai.
argument-hint: [scene-image-url]
disable-model-invocation: true
allowed-tools: Read, Bash(curl *), Write, Glob
---

# AIOFM Auto Instagram Post Creator

Workflow:
1. User provides a scene image URL
2. AI model image URL is loaded from `ai-model-url.txt`
3. Both images are sent to Fal.ai nano banana 2 — scene image as figure 1, AI model as figure 2
4. Fixed prompt: "replicate the exact image as in figure 1, but switch out the model in figure 1 with the model in figure 2"
5. Output saved to `output/instagram-posts/` and shown in chat

---

## Setup Requirements

| Item | Location |
|------|----------|
| AI model image URL | `ai-model-url.txt` — one line, public URL |
| Fal.ai API key | Environment variable `FAL_API_KEY` |

If either is missing, stop and tell the user exactly what's needed.

---

## Step 1: Gather Inputs

`$ARGUMENTS` is the scene image URL. If not provided, ask for it.

---

## Step 2: Load AI Model URL

Read `ai-model-url.txt` and store the URL as `AI_MODEL_URL`.
Stop if the file is missing or empty.

---

## Step 3: Show Preview and Request Approval

```
## Ready to Generate

**Scene image (figure 1):** [scene image URL]
**AI model (figure 2):** [AI_MODEL_URL]

**Prompt:** "replicate the exact image as in figure 1, but switch out the model in figure 1 with the model in figure 2"

Generate? (yes / no)
```

Do not call the API until the user confirms.

---

## Step 4: Call Fal.ai nano banana 2

Scene image is always first (`image_urls[0]`), AI model is always second (`image_urls[1]`).

```bash
curl -s -X POST https://fal.run/fal-ai/nano-banana-2/edit \
  -H "Authorization: Key $FAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "replicate the exact image as in figure 1, but switch out the model in figure 1 with the model in figure 2",
    "image_urls": ["SCENE_IMAGE_URL", "AI_MODEL_URL"],
    "num_images": 1,
    "resolution": "1K",
    "aspect_ratio": "4:5",
    "output_format": "png"
  }'
```

Extract the generated image URL from the response.
If the call fails, show the full error and stop.

---

## Step 5: Save Output

Save to: `output/instagram-posts/[YYYY-MM-DD].md`

```markdown
# Instagram Post — [Date]
**Date:** [date]

## Generated Image
![Result]([Fal.ai output URL])
Original scene: [scene image URL]
```

---

## Step 6: Present to User

Show the generated image URL in chat and display the saved file path.

End with:
> "Review the image and post when ready. Nothing has been published."

---

## Guardrails

- Never call Fal.ai without explicit user approval in Step 3
- Never auto-post — output is always for human review
- Never alter the fixed prompt sent to Fal.ai
- Scene image is always figure 1, AI model is always figure 2
- Never hardcode the API key — always use `$FAL_API_KEY`
- If the API returns an error, show it and stop
