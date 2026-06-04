---
name: Clinical Precision System
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#414751'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#727783'
  outline-variant: '#c1c6d3'
  surface-tint: '#065fae'
  primary: '#004583'
  on-primary: '#ffffff'
  primary-container: '#005dac'
  on-primary-container: '#bfd7ff'
  inverse-primary: '#a6c8ff'
  secondary: '#0058bb'
  on-secondary: '#ffffff'
  secondary-container: '#1471e6'
  on-secondary-container: '#fefcff'
  tertiary: '#733200'
  on-tertiary: '#ffffff'
  tertiary-container: '#984400'
  on-tertiary-container: '#ffcbaf'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d4e3ff'
  primary-fixed-dim: '#a6c8ff'
  on-primary-fixed: '#001c3a'
  on-primary-fixed-variant: '#004786'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc7ff'
  on-secondary-fixed: '#001a41'
  on-secondary-fixed-variant: '#004493'
  tertiary-fixed: '#ffdbc9'
  tertiary-fixed-dim: '#ffb68d'
  on-tertiary-fixed: '#321200'
  on-tertiary-fixed-variant: '#763300'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  data-mono:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
    letterSpacing: -0.01em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  input-group-gap: 12px
  container-padding: 24px
---

## Brand & Style

The brand personality of this design system is rooted in clinical authority, precision, and unwavering reliability. It is designed for high-stakes healthcare environments where clarity of data is paramount and cognitive load must be minimized. The emotional response should be one of "calm confidence"—reassuring the user that the information presented is accurate and professional.

The visual style is a hybrid of **Modern Corporate** and **Functional Minimalism**, featuring high-contrast data containers and a strict adherence to a structured grid. To ensure data integrity is visually reinforced, the system utilizes subtle structural borders and generous whitespace, avoiding unnecessary decorative elements that could distract from patient care.

## Colors

The color strategy prioritizes accessibility and semantic clarity. 

- **Primary Blue (#005dac):** Used for navigation, primary actions, and branding elements to establish a sense of institutional trust.
- **Success Green (#1e7e34):** Reserved for "Normal" ranges, stable patient vitals, and completed tasks.
- **Danger Red (#dc3545):** Strictly applied to malignant alerts, critical lab values, and destructive actions.
- **Neutral Grays:** A range of cool-toned grays used for backgrounds (`#f8f9fa`) and subtle UI borders (`#dee2e6`).
- **Data Borders:** A darker neutral (`#343a40`) is used specifically for outlining data tables and grouped numerical inputs to ensure sharp definition on medical-grade monitors.

## Typography

This design system utilizes **Hanken Grotesk** for headlines to provide a modern, sharp, and professional character. **Inter** is the workhorse for all body copy, labels, and data entry, chosen for its exceptional legibility and neutral tone.

Numerical data should always use a medium weight to ensure that lab values and vital signs are easily scannable. For dense clinical reports, the `body-sm` size is the standard to allow for maximum information density without sacrificing readability.

## Layout & Spacing

This design system employs a **Fixed Grid** approach for desktop dashboards to ensure that data visualizations remain consistent and predictable. 

- **Desktop:** 12-column grid with a 1440px max-width, 24px gutters, and 48px side margins.
- **Tablet:** 8-column fluid grid with 16px gutters and 24px margins.
- **Mobile:** 4-column fluid grid with 12px gutters and 16px margins.

The spacing rhythm is built on a 4px base unit. Numerical input groups should use a tight 12px gap between fields to indicate their relationship, while main sections are separated by a minimum of 32px or 48px to create a clear hierarchy of information.

## Elevation & Depth

To maintain a clean and professional appearance, this design system avoids heavy shadows and skeuomorphism. Instead, it relies on **Tonal Layers** and **Structured Outlines**.

- **Level 0 (Surface):** The main background uses a light neutral gray (`#f8f9fa`).
- **Level 1 (Cards/Containers):** Pure white (`#ffffff`) with a 1px border in a medium-gray (`#dee2e6`). 
- **Level 2 (Data Emphasis):** Data-heavy sections or grouped inputs use a darker 1px or 2px border (`#343a40`) to create a clear boundary between different patient records or diagnostic categories.
- **Overlays:** Only modals and dropdowns utilize a soft, low-opacity ambient shadow (Blur 12px, Opacity 8%, Color #000) to signify temporary interaction states.

## Shapes

The shape language is conservative and "Soft." A standard `0.25rem` (4px) radius is applied to most UI elements including buttons, input fields, and cards. This slight rounding softens the clinical environment without losing the feeling of precision and structure associated with sharp corners.

Pill-shaped elements are reserved exclusively for status indicators (e.g., "Active," "Discharged") to differentiate them from interactive buttons.

## Components

### Buttons
- **Primary:** Solid #005dac with white text. Used for "Save Record" or "Submit Diagnosis."
- **Secondary:** Outlined #005dac. Used for "Cancel" or "Go Back."
- **Critical Action:** Solid #dc3545. Used for "Flag Malignant" or "Delete Record."

### Input Fields (Numerical Groups)
Numerical inputs should be grouped within a container using a `dark-border` (1px, #343a40). Labels are positioned above the field in `label-md`. Suffixes (e.g., "mg/dL", "bpm") are placed inside the field, right-aligned, in a muted gray color.

### Result Cards
Result cards require high contrast. They use a white background with a prominent 4px left-accent border that changes color based on the result status:
- **Blue:** General Information
- **Green:** Normal/Healthy
- **Red:** Critical/Malignant Alert

### Data Tables
Tables should use a "Zebra-stripe" pattern with light gray rows. The header row must have a dark 2px bottom border to clearly separate labels from clinical data.

### Checkboxes & Radios
Standard 16px square (checkbox) and circle (radio) with a 2px Primary Blue border when selected. These should be large enough for easy selection in high-pressure environments.