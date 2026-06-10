# AiDa

**Artificial Intelligence Daily Assistant**

## Overview

AiDa is a multi-agent AI personal life optimization system designed to help users achieve their fitness and nutrition goals through natural conversation, personalized recommendations, memory, and behavioral analysis.

Unlike traditional fitness applications that rely on forms and menus, AiDa interacts with users conversationally, learns about them over time, remembers their preferences and goals, and adapts its recommendations accordingly.

---

# Problem Statement

Many users need guidance in multiple areas simultaneously:

* Fitness training
* Nutrition planning
* Progress monitoring
* Motivation and coaching

Current solutions often require several separate applications and significant manual effort.

AiDa unifies these functions into a single intelligent assistant.

---

# Project Objective

Develop an AI-powered assistant capable of:

* Understanding users through conversation
* Building and maintaining user profiles
* Generating personalized workout plans
* Generating personalized meal plans
* Analyzing meal images
* Tracking user progress
* Providing adaptive recommendations

---

# System Architecture

```text
                    USER
                      |
                      v

          Conversational Interface
                      |
                      v

                 Orchestrator
                      |

 ------------------------------------------------
 |                |              |              |
 v                v              v              v

Profile       Workout      Nutrition      Vision
Agent         Agent        Agent          Agent

                     |
                     v

              Progress Analyst

                     |
                     v

                Memory System

                     |
                     v

                 Goal Engine
```

---

# Components

## Orchestrator

Responsible for routing user requests to the appropriate agent.

Examples:

* Workout request → Workout Agent
* Meal request → Nutrition Agent
* Progress question → Progress Analyst

---

## Profile Agent

Responsible for collecting and maintaining user information.

Collected information:

* Name
* Age
* Weight
* Height
* Goal
* Available equipment
* Food preferences

---

## Workout Agent

Generates personalized workout plans based on:

* User goals
* Experience level
* Available equipment

Outputs:

* Workout schedules
* Exercise recommendations

---

## Nutrition Agent

Generates meal plans and nutritional recommendations based on:

* User goals
* Available foods
* Personal preferences

Outputs:

* Meal plans
* Nutritional advice

---

## Vision Agent

Analyzes meal images.

Outputs:

* Estimated calories
* Estimated protein
* Nutritional feedback

---

## Progress Analyst

Analyzes historical data and user behavior.

Outputs:

* Progress reports
* Behavioral insights
* Recommendations

Examples:

* Frequent missed workouts
* Recurring dietary issues
* Progress trends

---

## Memory System

Stores:

* User profiles
* Workout history
* Meal history
* Conversation history

This enables long-term personalization.

---

## Goal Engine

Maintains the user's objectives and ensures all recommendations align with them.

Example:

Current weight: 90 kg

Target weight: 80 kg

All generated plans should support this objective.

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Database

* SQLite

## AI Model

* OpenAI API or Gemini API

## Additional Libraries

* Pandas
* Pillow
* Python-dotenv

---

# Database Structure

## profiles

Stores user information.

Fields:

* id
* name
* age
* weight
* height
* goal
* equipment
* preferences

---

## meals

Stores meal history.

Fields:

* id
* user_id
* description
* calories
* protein
* date

---

## workouts

Stores workout history.

Fields:

* id
* user_id
* workout
* completed
* date

---

## conversations

Stores conversation history.

Fields:

* id
* user_id
* user_message
* ai_response
* timestamp

---

# Minimum Viable Product (MVP)

The following features must be completed before the deadline:

* Conversational onboarding
* User memory
* Personalized workout generation
* Personalized meal planning
* Meal image analysis
* Progress recommendations

---

# Future Improvements

Potential extensions beyond the course project:

* Weight tracking dashboard
* Weekly progress summaries
* Wearable device integration
* Advanced analytics
* Mobile application
* Goal prediction models

---

# Development Timeline

## Friday

* Architecture design
* Database design
* Project structure setup

## Saturday

* API setup
* Memory system implementation
* Profile Agent implementation

## Sunday

* Conversational onboarding

## Monday

* Workout Agent

## Tuesday

* Nutrition Agent

## Wednesday

* Vision Agent

## Thursday

* Progress Analyst
* Testing
* Bug fixes

## Friday

* Buffer day
* Report finalization
* Presentation preparation

---

# Project Status

Current Status: Day 1 Complete

Completed:

* Project definition
* System architecture
* Database design
* Project structure

Next Milestone:

Implement Profile Agent and Memory System.
