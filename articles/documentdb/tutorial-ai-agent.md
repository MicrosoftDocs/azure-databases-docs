---
title: 'Tutorial: Build an AI travel agent with LangChain'
description: Learn how to create an autonomous AI agent that processes traveler inquiries and bookings using Azure DocumentDB's vector database and document store capabilities. Build a sample application with Python FastAPI and React.
author: seesharprun
ms.author: sidandrews
ms.topic: tutorial
ms.date: 10/20/2025
ms.custom:
  - devx-track-js
  - devx-track-python
  - sfi-image-nochange
  - sfi-ropc-blocked
# Customer Intent: As a developer, I want to build an AI agent that can handle travel bookings and inquiries using Azure DocumentDB so that I can create intelligent applications with unified memory systems.
---

# Tutorial: Build an AI travel agent with Azure DocumentDB and LangChain

This tutorial shows you how to build an autonomous AI agent that processes traveler inquiries and bookings for a cruise line. The AI agent uses the LangChain Agent framework for planning, tool usage, and perception. The agent then combines these features with Azure DocumentDB's vector database and document store capabilities for a unified memory system.

The sample agent operates within a Python FastAPI backend and supports user interactions through a React JavaScript user interface. This implementation demonstrates how AI agents advance beyond basic chatbots to carry out complex tasks based on natural language that traditionally require coded logic.

In this tutorial, you learn how to:

> [!div class="checklist"]
>
> - Set up Azure DocumentDB with vector search capabilities
> - Load travel documents and create vector embeddings
> - Build an AI agent using Python FastAPI and LangChain
> - Implement agent tools for vacation lookup, itinerary search, and booking
> - Create a React web interface for user interactions
> - Test the complete AI agent solution
>

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- An account for the OpenAI API or Azure OpenAI Service.

- An integrated development environment, such as Visual Studio Code.

- Python 3.11.4 or later installed in the development environment.

- Node.js installed for the React frontend.

## Download the sample project

All the code and sample datasets are available in the [Travel AI Agent GitHub repository](https://github.com/jonathanscholtes/Travel-AI-Agent-React-FastAPI-and-Cosmos-DB-Vector-Store). 

1. Clone or download the repository (<https://github.com/jonathanscholtes/Travel-AI-Agent-React-FastAPI-and-Cosmos-DB-Vector-Store>) to your local development environment.

1. Navigate to the project directory and explore the structure:
   
    - `/loader`: Contains Python code for loading sample documents and vector embeddings in Azure DocumentDB
    
    - `/api`: Contains the Python FastAPI project for hosting the AI travel agent
    
    - `/web`: Contains code for the React web interface

## Load travel documents into Azure DocumentDB

The `/loader` directory contains a Python project for loading sample travel documents into Azure DocumentDB and creating the necessary vector embeddings.

1. Navigate to the `/loader` directory in your terminal.

1. Create a Python virtual environment:

    ```console
    python -m venv venv
    ```

1. Activate the virtual environment:

    ```console
    # On Windows
    venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

1. Install the required dependencies:

    ```console
    python -m pip install -r requirements.txt
    ```

1. Create a `.env` file in the `/loader` directory with your connection details:

    ```env
    OPENAI_API_KEY="<your OpenAI key>"
    MONGO_CONNECTION_STRING="mongodb+srv:<your connection string from Azure DocumentDB>"
    ```

1. The `main.py` file serves as the central entry point for loading data. It processes sample travel data including ship and destination information, then generates travel itinerary packages.

1. Run the data loading script from the `/loader` directory. The script performs these operations:

    - Reads ship and destination data from JSON files

    - Creates five itinerary packages using the `ItineraryBuilder`

    - Saves itinerary packages to the `itinerary` collection

    - Saves destinations to the `destinations` collection

    - Creates vector embeddings for ships in the `ships` collection

    - Adds a text search index to ship names

    ```console
    python main.py
    ```

1. Verify the output shows successful completion:

    ```output
    --build itinerary--
    --load itinerary--
    --load destinations--
    --load vectors ships--
    ```

## Build the AI travel agent API

The AI travel agent is hosted through a Python FastAPI backend that integrates with the frontend interface and processes agent requests by grounding large language model (LLM) prompts against Azure DocumentDB data.

1. Navigate to the `/api` directory in your terminal.

1. Create and activate a Python virtual environment:

    ```console
    python -m venv venv
    
    # On Windows
    venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

1. Install the required dependencies:

    ```console
    python -m pip install -r requirements.txt
    ```

1. Create a `.env` file in the `/api` directory:

    ```env
    OPENAI_API_KEY="<your OpenAI key>"
    MONGO_CONNECTION_STRING="mongodb+srv:<your connection string from Azure DocumentDB>"
    ```

1. Run the FastAPI application from the `/api` directory:

    ```console
    python app.py
    ```

1. The server starts on `http://127.0.0.1:8000` by default.

1. Explore the API endpoints by accessing the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### Test the AI agent functionality

Test that the AI agent functions as expected.

1. In the Swagger interface, test the session endpoint:

    - Navigate to `/session/` and select **Try it out**

    - Execute the request to get a session ID for tracking conversation history

1. Test the agent chat functionality:

    - Navigate to `/agent/agent_chat` and select **Try it out**

    - Use this example input to test the agent:
  
    ```json
    {
      "input": "I want to take a relaxing vacation.",
      "session_id": "your-session-id-from-step-1"
    }
    ```

1. The agent should respond with cruise recommendations based on vector similarity search, demonstrating the integration between the LLM and Azure DocumentDB.

## Create the React web interface

The web interface provides a user-friendly way to interact with the AI travel agent through a conversational interface.

### Set up the React environment

1. Go to the `/web` directory in your terminal.

1. Install the project dependencies:

    ```console
    npm ci
    ```

1. Create a `.env` file in the `/web` directory:

    ```env
    REACT_APP_API_HOST=http://127.0.0.1:8000
    ```

### Launch the web application

1. Start the React development server:

    ```console
    npm start
    ```

1. The application opens automatically in your default browser, typically at `http://localhost:3000`.

1. The interface shows a travel website with cruise ship and destination images.

### Test the complete solution

1. On the main page, select **Effortlessly plan your voyage** to open the travel assistant chat interface.

1. The chat interface opens in a dialog with a prepopulated message: "I want to take a relaxing vacation."

1. Select **Submit** to send the message to the AI agent.

1. The agent responds with cruise recommendations based on your input, demonstrating:

    - Natural language processing

    - Vector similarity search against Azure DocumentDB

    - Conversational memory across the session

    - HTML-formatted responses in the chat interface

1. See the full range of agent capabilities by continuing the conversation. Ask about specific ships, itineraries, or making bookings.

## Understand the AI agent architecture

The AI agent implementation follows a layered architecture that separates concerns and enables maintainability.

### Service Layer Components

The service layer contains the core business logic and LangChain Agent implementation:

- **Agent Initialization**: The `init.py` module sets up the ChatOpenAI model, agent tools, and conversation history.

- **Agent Tools**: Three main tools handle vacation lookup, itinerary search, and cruise booking.

- **Memory Management**: Conversation history is stored in Azure DocumentDB using session identifiers.

### Agent Tools Functionality

The AI agent uses three specialized tools.

1. **vacation_lookup**: Conducts vector search against Azure DocumentDB to find relevant travel information.

1. **itinerary_lookup**: Retrieves cruise package details and schedules for specific ships.

1. **book_cruise**: Handles cruise package bookings with passenger information validation.

### Data Layer Integration

The data layer handles all interactions with Azure DocumentDB.

- **Vector Search**: Similarity search with scoring for travel recommendations.

- **Document Storage**: Structured data for ships, destinations, and itineraries.

- **Conversation History**: Session-based chat message storage.

## Clean up resources

If you no longer need the resources created in this tutorial, you can clean them up to avoid ongoing charges:

1. In the Azure portal, navigate to your Azure DocumentDB account.

1. If you created a dedicated resource group for this tutorial, delete the entire resource group.

1. Otherwise, delete the specific collections created:

   - `travel.itinerary`

   - `travel.destinations`

   - `travel.ships`

   - `travel.history`

## Next step

> [!div class="nextstepaction"]
> [Learn about vector search in Azure DocumentDB](vector-search.md)
