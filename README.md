"# newtv1" 
This is newtv1. An AI automation bot.

Core Modules Overview
Module	Purpose
core/	Handles startup, voice input/output, CLI & GUI interface.
task_routing/	Smart command dispatcher that maps natural language to functions.
tasks/	Real-world system control modules — apps, media, browser, productivity, etc.
llm/	Fine-tuned small language model for local inference.
data/	Persistent memory and runtime logs.

How It Works
User Input (voice or text) →
Task Router analyzes intent →
Routes to the correct module in /tasks →
Executes the function (e.g. open browser, play music, check email) →
Speaks the response via TTS
(LLM integration layer processes more complex reasoning once added.)'
