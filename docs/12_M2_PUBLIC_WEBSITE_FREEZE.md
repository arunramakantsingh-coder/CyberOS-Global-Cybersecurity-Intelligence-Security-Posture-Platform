# CyberOS M2 Public Website Freeze

**Status:** FROZEN
**Freeze baseline:** `81da2a1cface98479f6e92c8afea8830619ca618`
**Primary development branch:** `foundation/m2-product-platform`
**Frozen snapshot branch:** `release/m2-public-website-frozen`

## Purpose

The CyberOS public commercial website is now a protected product surface. Its visual language, layout system, fixed top navigation, responsive behavior, section ordering and public messaging are considered the approved M2 baseline.

## Frozen Scope

The following public experience is frozen unless a future change is explicitly classified as a public-website change:

- fixed top navigation;
- public brand/header treatment;
- hero section;
- platform positioning;
- module catalogue presentation;
- compliance section;
- Demo World presentation;
- pricing presentation;
- trust/security section;
- footer;
- responsive breakpoints;
- horizontal overflow prevention;
- vertical page flow and section separation;
- public visual language and typography.

## Development Rule

**Do not modify the frozen public website while implementing internal CyberOS modules.**

A request for Threat Intelligence, Vulnerability, Security Posture, Web Security, Network & Hardening, Compliance, Cyber AI or Reports must modify only that module's implementation surface and its directly required shared contracts.

Changes to shared layout/navigation are prohibited unless the task is explicitly a navigation/platform-shell task.

## Snapshot / Recovery

The approved M2 website snapshot is preserved on:

`release/m2-public-website-frozen`

The snapshot is the recovery point if a later module implementation accidentally affects the public experience.

## Verification Requirement

Before every module merge/commit:

1. verify the public website route;
2. verify fixed top navigation;
3. verify no horizontal overflow;
4. verify responsive layout at desktop/tablet/mobile widths;
5. verify all public sections remain reachable;
6. verify the frozen visual baseline has not changed unexpectedly.

## Intent

CyberOS development now proceeds by **module isolation** rather than by repeatedly changing the global UI shell.
