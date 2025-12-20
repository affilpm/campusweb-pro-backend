# School Website Implementation Plan

## Overview

This document outlines the complete implementation of the production-ready school website with:
- Fully admin-managed content
- Complete public pages (Home, About, Academics, Admissions, Contact, Gallery)
- Clean, professional, real-world school website UX
- Strong SEO and accessibility

---

## Architecture

### Backend (Django + DRF)

**Location:** `/backend/`

**Models:** (in `content/models.py`)
- **Singleton Models:** SiteSettings, HeroSection, AboutSection, PrincipalMessage, VisionMission, AdmissionSettings, AcademicsPage, AboutPage, ContactPage
- **List Models:** Notice, Event, GalleryCategory, GalleryImage, Facility, AcademicHighlight, Testimonial, QuickLink, Achievement, AdmissionStep, ClassCategory, Subject, TimelineEvent, ManagementMember, Download, ContactSubmission, PageSEO

**API Structure:**
- **Public APIs:** `/api/public/` - Read-only endpoints
- **Admin APIs:** `/api/admin/content/` - Protected CRUD endpoints

### Frontend (Next.js App Router)

**Location:** `/frontend/`

**Public Pages:**
- `/` - Homepage
- `/about` - About Us page
- `/academics` - Academics page
- `/admissions` - Admissions page
- `/contact` - Contact page with form
- `/gallery` - Photo gallery

**Admin Pages:** `/secure-admin/`
- `/secure-admin/login` - Hidden admin login
- `/secure-admin/` - Dashboard
- Various management pages for content

---

## Public Pages Details

### 1. Homepage (`/`)
- Hero section with school name and banner
- About section preview
- Principal's message
- Vision & Mission
- Notices ticker
- News & Events carousel
- Facilities grid
- Academic highlights
- Photo gallery preview
- Testimonials
- Admission status banner (CTA)
- Footer with contact info

### 2. About Page (`/about`)
- Hero section with title
- School history (rich text)
- Vision & Mission cards
- Principal profile
- Management team grid
- School timeline (milestones)
- Affiliation details
- Infrastructure overview

### 3. Academics Page (`/academics`)
- Hero section
- Curriculum overview
- Class categories with subjects
- Teaching methodology
- Academic calendar download

### 4. Admissions Page (`/admissions`)
- Admission status banner (Open/Closed)
- Admission process steps
- Eligibility criteria
- Required documents list
- Fee structure (content + PDF download)
- Enquiry contact info

### 5. Contact Page (`/contact`)
- Address, phone, email
- Office hours
- Contact form (submits to backend)
- Google Maps embed

### 6. Gallery Page (`/gallery`)
- Category filter
- Image grid
- Lightbox modal

---

## Admin CMS Features

### Content Management
1. **Site Settings:** School name, logo, contact info, social links
2. **Hero Section:** Banner image, title, CTA
3. **About Section:** History, stats, image
4. **Principal Message:** Photo, message, qualifications
5. **Vision & Mission:** Vision, mission, values text
6. **Notices:** CRUD with status, importance flags
7. **Events:** CRUD with images, dates, featured flags
8. **Gallery:** Categories + images management
9. **Facilities:** CRUD with icons and images
10. **Testimonials:** CRUD with ratings
11. **Achievements:** Awards and milestones
12. **Admissions:** Status toggle, steps, eligibility, documents, fees
13. **Academics:** Curriculum, class categories, subjects
14. **About Page:** History content, timeline, management team
15. **Downloads:** Circulars, PDFs by category
16. **Contact:** Office hours, map embed, form submissions view
17. **SEO:** Per-page meta titles, descriptions, OG images

---

## API Endpoints

### Public (Read-only)
```
GET /api/public/home/          - All homepage data
GET /api/public/about/         - About page data
GET /api/public/academics/     - Academics page data
GET /api/public/admissions/    - Admissions page data
GET /api/public/contact/       - Contact page data
POST /api/public/contact/submit/ - Submit contact form
GET /api/public/notices/       - List notices
GET /api/public/events/        - List events
GET /api/public/events/<slug>/ - Event detail
GET /api/public/gallery/       - Gallery images
GET /api/public/achievements/  - Achievements list
GET /api/public/downloads/     - Downloads list
GET /api/public/seo/<slug>/    - Page SEO settings
```

### Admin (Authenticated)
```
/api/admin/content/site-settings/  - GET/PUT
/api/admin/content/hero/           - GET/PUT
/api/admin/content/about/          - GET/PUT
/api/admin/content/principal/      - GET/PUT
/api/admin/content/vision-mission/ - GET/PUT
/api/admin/content/notices/        - GET/POST/PUT/DELETE
/api/admin/content/events/         - GET/POST/PUT/DELETE
/api/admin/content/gallery/        - Categories + Images CRUD
/api/admin/content/facilities/     - GET/POST/PUT/DELETE
/api/admin/content/testimonials/   - GET/POST/PUT/DELETE
/api/admin/content/achievements/   - GET/POST/PUT/DELETE
/api/admin/content/admissions/     - Settings + Steps CRUD
/api/admin/content/academics/      - Page + Categories + Subjects
/api/admin/content/about/          - Page + Timeline + Management
/api/admin/content/downloads/      - GET/POST/PUT/DELETE
/api/admin/content/contact/        - Page + Submissions
/api/admin/content/seo/            - GET/POST/PUT/DELETE
```

---

## Content Flow

```
+------------------+     +------------------+     +------------------+
|   Admin Panel    | --> |  Django Backend  | --> |   Next.js SSR    |
|  (Hidden Routes) |     |   (REST APIs)    |     |  Public Website  |
+------------------+     +------------------+     +------------------+
         |                        |                        |
    Admin edits            Stores content            Fetches via
    content via            in PostgreSQL/           ISR (60s cache)
    forms/uploads          SQLite models            for performance
```

---

## Security Features

1. **Hidden Admin Routes:** No links visible to public visitors
2. **JWT Authentication:** Access + Refresh tokens for admin
3. **CORS Configuration:** Proper origin restrictions
4. **Protected APIs:** Admin endpoints require authentication
5. **No Public Login:** No login buttons on public pages

---

## Running the Project

### Backend
```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py seedcontent  # Seed initial data
python manage.py runserver 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Access:
- Public site: http://localhost:3000
- Admin: http://localhost:3000/secure-admin/login

---

## SEO Features

- Dynamic meta tags per page
- Semantic HTML structure
- Mobile-first responsive design
- Fast page loads with ISR
- Image optimization
- Structured data ready

---

## Next Steps

1. **Content Population:** Add real content via admin panel
2. **Image Optimization:** Add school photos via admin
3. **Testing:** Test all pages for responsiveness
4. **Accessibility Audit:** WCAG compliance check
5. **Performance Optimization:** Lighthouse audit
6. **Deployment:** Configure production servers
