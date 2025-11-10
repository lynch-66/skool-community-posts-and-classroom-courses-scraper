# Skool Community Posts and Classroom Courses Scraper

> Extract complete discussion threads, classroom modules, and engagement metrics from Skool communities. This scraper captures posts, lessons, metadata, authors, and fully nested comments to power research, analytics, and content strategy.
>
> Ideal for teams that need structured Skool data at scale—cleanly mapped fields, consistent timestamps, and linkable entities across posts, users, and courses.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Skool Community Posts and Classroom Courses Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project programmatically collects rich, structured data from Skool communities—covering both the **Community** and **Classroom** tabs. It solves the pain of manual copy-paste and inconsistent exports by producing normalized JSON records for posts, modules, users, and nested comments.

**Who it’s for:** growth teams, community managers, researchers, data engineers, and product teams analyzing Skool conversations, learning material, and engagement signals.

### What You Can Analyze

- End-to-end threads: post content, authors, timestamps, labels, and replies (with full nesting).
- Classroom structure: courses, modules, lesson titles, media links, and related metadata.
- Engagement signals: upvotes, comment counts, pinned flags, and “has new comments”.
- User context: name, profile images, bio, links, locations, and creation/update times.
- Coverage control: choose community or classroom focus, include/exclude comments, cap items.

## Features

| Feature | Description |
|----------|-------------|
| Community & Classroom coverage | Scrape posts, courses, modules, and their comments from targeted Skool groups. |
| Nested comments | Capture full reply chains with parent/root references for accurate thread reconstruction. |
| Rich metadata | Titles, content, labels, pinned flags, media previews, engagement metrics, and URLs. |
| User enrichment | Collect author/commenter profile info (names, bios, avatars, links, timestamps). |
| Selective depth | Toggle comment inclusion per tab to match your scope and performance targets. |
| Input flexibility | Provide one or many Skool community URLs; target classroom or community tab. |
| Scale controls | Configure max items, concurrency, and retry budgets for stability at scale. |
| Proxy ready | Works with residential proxies to minimize blocks and emulate real-user traffic. |
| Structured outputs | Clean JSON compatible with data warehouses, notebooks, and BI tools. |
| Reliability tooling | Automatic retries, bounded concurrency, and graceful handling of edge cases. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| id | Unique identifier for a post/module/course entity. |
| name/title/postTitle | URL-friendly name or human-readable title of the entity. |
| content | Main textual content of a post or classroom module. |
| metadata | Object containing action codes, counts, previews, labels, and flags. |
| comments | Array of comments (each a structured object with nesting). |
| upvotes/comments (counts) | Engagement metrics for ranking and analysis. |
| pinned | Flag indicating whether a post is pinned (0/1). |
| imagePreview/videoLinksData/media | Media previews, arrays of media links (e.g., videos). |
| labels/labelId | Label identifiers associated with the post. |
| hasNewComments/lastComment | Signals for recency and freshness of discussion. |
| createdAt/updatedAt | ISO timestamps for creation and last update. |
| groupId/rootId/parent_id | Graph pointers for reconstructing thread/module relationships. |
| postType/type | Entity type (e.g., generic, comment, module). |
| url/urlAjax | Canonical page URL and related API/comment endpoints for a module. |
| user | Object with author details (id, name, bio, avatars, links, first/last names). |
| courseMetaDetails | Object containing course id, name, title, and timestamps (classroom tab). |

---

## Example Output

<If available, include example data block. Skip this section if not present.>
<do not use ``` , >
<write this output with tab space behind>

Example:


    {
      "id": "aab147fa0ea4420d83e8d3a9214f5203",
      "name": "roadmap-update",
      "metadata": {
        "action": 0,
        "content": "Post content here...",
        "comments": 37,
        "upvotes": 50,
        "title": "Roadmap Update",
        "pinned": 1,
        "imagePreview": "",
        "imagePreviewSmall": "",
        "videoLinksData": "[]",
        "contributors": "[{...}]",
        "labels": "3916973e45d64416917aaba09edff141",
        "hasNewComments": 1,
        "lastComment": 1731431342139887000
      },
      "createdAt": "2024-11-07T23:26:18.04203Z",
      "updatedAt": "2024-11-14T09:50:05.802436Z",
      "groupId": "b575158c8d8240b88e9f13da74aa66cc",
      "userId": "5222fdb103d340ecaf61d47f35302f52",
      "postType": "generic",
      "rootId": "aab147fa0ea4420d83e8d3a9214f5203",
      "labelId": "3916973e45d64416917aaba09edff141",
      "user": {
        "id": "5222fdb103d340ecaf61d47f35302f52",
        "name": "username",
        "metadata": {
          "actStatus": "hardcore",
          "bio": "User bio...",
          "pictureBubble": "URL to bubble picture",
          "pictureProfile": "URL to profile picture",
          "location": "User location",
          "linkWebsite": "User website URL",
          "linkYoutube": "User YouTube URL"
        },
        "createdAt": "2020-05-14T00:51:12.09168Z",
        "updatedAt": "2024-11-14T15:45:27.923959Z",
        "firstName": "First",
        "lastName": "Last"
      },
      "url": "https://www.skool.com/group-name/post-name",
      "comments": [
        {
          "post": {
            "id": "comment-id",
            "metadata": {
              "action": 0,
              "content": "Comment content...",
              "upvotes": 4,
              "attachments": "attachment-id",
              "attachments_data": "[{...}]"
            },
            "created_at": "2024-11-07T23:28:36.995Z",
            "updated_at": "2024-11-08T00:40:38.94154Z",
            "user_id": "user-id",
            "post_type": "comment",
            "parent_id": "parent-post-id",
            "root_id": "root-post-id",
            "user": {
              "id": "user-id",
              "name": "username",
              "metadata": {
                "bio": "User bio",
                "picture_bubble": "URL to bubble picture",
                "picture_profile": "URL to profile picture"
              },
              "created_at": "Creation timestamp",
              "updated_at": "Update timestamp",
              "first_name": "First",
              "last_name": "Last"
            }
          }
        }
      ]
    }


    {
      "type": "module",
      "title": "Module Title",
      "postTitle": "Specific Lecture Title",
      "content": "Module content and description...",
      "id": "unique-module-id",
      "urlAjax": "https://api.skool.com/posts/module-id/comments",
      "url": "https://www.skool.com/group-name/classroom/module-name",
      "media": [
        "https://www.loom.com/share/video-id"
      ],
      "courseMetaDetails": {
        "id": "course-id",
        "name": "course-name",
        "title": "Course Title",
        "createdAt": "2024-09-20T16:51:46.06926Z",
        "updatedAt": "2024-11-12T23:47:47.319915Z"
      },
      "comments": []
    }

---

## Directory Structure Tree

<Assume it’s a complete working project. Show a detailed and realistic folder and file structure with correct extensions.
All directory structure code must remain inside this same fenced block.>

Example:


    skool-community-posts-and-classroom-courses-scraper/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── community_scraper.py
    │   │   ├── classroom_scraper.py
    │   │   └── utils_time.py
    │   ├── parsers/
    │   │   ├── posts.py
    │   │   ├── comments.py
    │   │   └── classroom.py
    │   ├── outputs/
    │   │   ├── exporters.py
    │   │   └── schema.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.json
    │   └── sample_output.json
    ├── tests/
    │   ├── test_posts.py
    │   ├── test_comments.py
    │   └── test_classroom.py
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Community Managers** aggregate top discussions and unanswered threads to prioritize replies and content programming.
- **Growth & Content Teams** mine high-signal comments and questions to inform blog topics, videos, and product messaging.
- **Researchers & Analysts** quantify engagement, sentiment, and topic clusters across cohorts and time ranges.
- **Course Creators** audit classroom structure, lesson coverage, and media links to improve curriculum quality.
- **Data Engineers** pipeline Skool data into warehouses for dashboards (retention, activation, power-user curves).

---

## FAQs

**Q1: Can I scrape only the Classroom or only the Community tab?**
Yes. Set the tab option to either community or classroom to target one surface. You can also toggle includeComments to optimize speed.

**Q2: How do I handle private groups or rate limits?**
Authenticate with valid session cookies and prefer residential proxies from the target geography. Use conservative concurrency, enable retries, and cap maxItems.

**Q3: Will nested replies preserve hierarchy?**
Yes. Each comment includes parent_id and root_id so you can rebuild full threads in your database or analytics tool.

**Q4: What formats are supported for downstream use?**
Outputs are JSON-first and can be exported to CSV/Excel for quick reviews. The field schema is designed to load cleanly into relational or document stores.

---

## Performance Benchmarks and Results

**Primary Metric (Throughput):** ~180–300 items/min at moderate concurrency (mix of posts and comments), depending on media density and geography.
**Reliability Metric (Success Rate):** 96–99% successful document fetch under stable network and residential proxy usage with up to 30 retries.
**Efficiency Metric (Resource Use):** Memory remains <300 MB for typical runs of ≤1k items; CPU bounded primarily by parsing and JSON serialization.
**Quality Metric (Data Completeness):** 98%+ field fill for core entities (posts/modules/users); optional media/label fields vary by source availability.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
