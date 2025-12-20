// Type definitions for public homepage data

export interface SiteSettings {
  school_name: string;
  school_motto: string;
  school_logo: string | null;
  favicon: string | null;
  address: string;
  phone: string;
  email: string;
  facebook_url: string;
  twitter_url: string;
  instagram_url: string;
  youtube_url: string;
  footer_text: string;
}

export interface HeroSection {
  title: string;
  subtitle: string;
  background_image: string | null;
}

export interface AboutSection {
  title: string;
  content: string;
  image: string | null;
  established_year: number;
  students_count: string;
  teachers_count: string;
}

export interface PrincipalMessage {
  name: string;
  title: string;
  photo: string | null;
  message: string;
  qualification: string;
}

export interface VisionMission {
  vision_title: string;
  vision_content: string;
  mission_title: string;
  mission_content: string;
  values_title: string;
  values_content: string;
}

export interface Notice {
  id: number;
  title: string;
  content: string;
  attachment: string | null;
  is_important: boolean;
  publish_date: string;
}

export interface Event {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content?: string;
  image: string | null;
  event_date: string | null;
  is_featured: boolean;
}

export interface GalleryImage {
  id: number | string;
  title: string;
  image: string;
  category: number | null;
  category_name: string | null;
  caption: string;
  is_featured: boolean;
}

export interface FacilityGalleryImage {
  id: number | string;
  image: string;
  caption: string;
  order: number;
}

export interface Facility {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  image: string | null;
  gallery?: FacilityGalleryImage[];
}

export interface AcademicHighlight {
  id: number;
  title: string;
  value: string;
  icon: string;
}

export interface Testimonial {
  id: number;
  name: string;
  role: string;
  photo: string | null;
  content: string;
  rating: number;
}

export interface QuickLink {
  id: number;
  title: string;
  url: string;
  open_in_new_tab: boolean;
}

export interface GeneralInfo {
  id: number;
  title: string;
  value: string;
  order: number;
}

export interface HomepageData {
  site_settings: SiteSettings;
  hero: HeroSection;
  about: AboutSection;
  principal: PrincipalMessage;
  vision_mission: VisionMission;
  notices: Notice[];
  events: Event[];
  gallery: GalleryImage[];
  facilities: Facility[];
  academics: AcademicHighlight[];
  achievements: Achievement[];
  testimonials: Testimonial[];
  quick_links: QuickLink[];
  general_info: GeneralInfo[];
}

// Achievement
export interface Achievement {
  id: number;
  title: string;
  description: string;
  image: string | null;
  year: number | null;
  is_featured: boolean;
}

// Admission Step
export interface AdmissionStep {
  step_number: number;
  title: string;
  description: string;
}

// Admission Settings
// Admission Settings
export interface AdmissionSettings {
  is_open: boolean;
  hero_title: string;
  hero_subtitle: string;
  overview_title: string;
  overview_content: string;
  eligibility_title: string;
  eligibility_content: string;
  documents_required: string;
  contact_info: string;
  application_form_link: string;
  steps: AdmissionStep[];
  site_settings: SiteSettings;
  quick_links: QuickLink[];
}

// Subject
export interface Subject {
  id: number;
  name: string;
  description: string;
  icon: string;
}

// Class Category
export interface ClassCategory {
  id: number;
  name: string;
  description: string;
  classes_range: string;
  image: string | null;
  subjects: Subject[];
}

// Academics Page
export interface AcademicsPageData {
  hero_title: string;
  hero_subtitle: string;
  curriculum_title: string;
  curriculum_content: string;
  curriculum_image: string | null;
  methodology_title: string;
  methodology_content: string;
  calendar_title: string;
  calendar_file: string | null;
  class_categories: ClassCategory[];
  site_settings: SiteSettings;
  quick_links: QuickLink[];
}

// Timeline Event
export interface TimelineEvent {
  year: number;
  title: string;
  description: string;
  image: string | null;
}

// Management Member
export interface ManagementMember {
  name: string;
  designation: string;
  photo: string | null;
  bio: string;
}

// About Page
export interface AboutPageData {
  hero_title: string;
  hero_subtitle: string;
  history_title: string;
  history_content: string;
  history_image: string | null;
  infrastructure_title: string;
  infrastructure_content: string;
  affiliation_title: string;
  affiliation_content: string;
  cbse_affiliation_no: string;
  timeline: TimelineEvent[];
  management: ManagementMember[];
  about_section: AboutSection;
  principal: PrincipalMessage;
  vision_mission: VisionMission;
  facilities: Facility[];
  site_settings: SiteSettings;
  quick_links: QuickLink[];
}

// Download
export interface Download {
  id: number;
  title: string;
  file: string;
  category: string;
  description: string;
  created_at: string;
}

// Contact Page
export interface ContactPageData {
  title: string;
  subtitle: string;
  office_hours: string;
  google_map_embed: string;
  site_settings: SiteSettings;
  quick_links: QuickLink[];
}

// Page SEO
export interface PageSEO {
  page_slug: string;
  title: string;
  meta_description: string;
  meta_keywords: string;
  og_image: string | null;
}

