#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#
# Author : Mithilesh Mohanty

library(shiny)
library(udpipe)
library(textrank)
library(lattice)
library(igraph)
library(ggraph)
library(ggplot2)
library(wordcloud)
library(stringr)
library(dplyr)



# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  datasetInput <- reactive({
      if (is.null(input$fileText)) {   
      return(NULL) 
      }else{
        textData <- readLines(input$fileText[1,"datapath"])  
        textData  =  str_replace_all(textData, "<.*?>", "")
        textData <- str_replace_all(textData, "[[:punct:]]", "")
        textData <- str_replace_all(textData, "[[:digit:]]+", "")
        textData <- str_replace_all(textData, "\\s+", " ")
        textData <- tolower(textData)
        englishModel = udpipe_load_model("./Data/english-ud-2.0-170801.udpipe")
        anotatedDoc <- udpipe_annotate(englishModel, x = textData)
        anotatedDoc <- as.data.frame(anotatedDoc)
        anotatedDoc
      }
  })
  
  observeEvent(input$checkButton, {
    datasetInput <- reactive({
      if (is.null(input$fileText)) {   
        return(NULL) 
      }else{
        textData <- readLines(input$fileText[1,"datapath"])  
        textData  =  str_replace_all(textData, "<.*?>", "")
        textData <- str_replace_all(textData, "[[:punct:]]", "")
        textData <- str_replace_all(textData, "[[:digit:]]+", "")
        textData <- str_replace_all(textData, "\\s+", " ")
        textData <- tolower(textData)
        englishModel = udpipe_load_model("./Data/english-ud-2.0-170801.udpipe")
        anotatedDoc <- udpipe_annotate(englishModel, x = textData)
        anotatedDoc <- as.data.frame(anotatedDoc)
        anotatedDoc
      }
    })
  })
  
  observeEvent(input$downloadButton, {
    temp <- datasetInput()
    write.csv(temp,file = file.choose(new = T))
  })
   
  output$annotatedDocumentContent <- renderDataTable({ 
    temp <- datasetInput()
    drops <- c("sentence")
    anotatedDoc <- temp[ , !(names(temp) %in% drops)]
    head(anotatedDoc,100)
  }, options = list(
    pageLength = 100,
    initComplete = I('function(setting, json) { alert("Loading Completed"); }')
  ))
  

  output$nounCaption <- renderText(
    if (input$WordCloud=='V'){
      return(NULL)
      
    }else{
      "WordCloud with Noun"
    }
      
    
  )
  output$verbCaption <- renderText(
    if (input$WordCloud=='N'){
      return(NULL)
     
    }else{
      "WordCloud with Verb"
    }
    
  )
  
  wordcloud_rep <- repeatable(wordcloud)
  
  output$wordCloudNoun <- renderPlot({ 
    if (input$WordCloud=='V'){
      return(NULL)
      
    }else{
    annotateData <- datasetInput()
    dataNouns =  subset(annotateData, upos %in% "NOUN")
    dataNouns = txt_freq(dataNouns$lemma)
    wordcloud_rep(words = dataNouns$key, 
             freq = dataNouns$freq, 
             min.freq = 3, 
             max.words = 100,
             random.order = FALSE, scale=c(10,0.5),
             colors = "Red")
    }
    
  })
  
  output$wordCloudVerb <- renderPlot({ 
    if (input$WordCloud=='N'){
      return(NULL)
      
    }else{
    annotateData <- datasetInput()
    dataVerbs = subset(annotateData, upos %in% "VERB")
    dataVerbs = txt_freq(dataVerbs$lemma)
    wordcloud_rep(words = dataVerbs$key, 
              freq = dataVerbs$freq, 
              min.freq = 3, 
              max.words = 100,
              random.order = FALSE, scale=c(10,0.5),
              colors = "black")
    }
  })
  output$coOccurance <- renderPlot({ 
    if (input$cooccurance=='A'){
      return(NULL)
      
    }else{
    annotateData <- datasetInput()
    coocurranceData <- cooccurrence(x = annotateData$lemma,  relevant = annotateData$upos %in% c("NOUN", "ADJ"))
    wordnetwork <- graph_from_data_frame(head(coocurranceData, 30))
    windowsFonts(Times=windowsFont("Times New Roman"))
    ggraph(wordnetwork, layout = "kk") +
      geom_edge_link(aes(width = cooc, edge_alpha = cooc), edge_colour = "red") +
      geom_node_text(aes(label = name), col = "black", size = 6) +
      theme_graph(base_family = "Times New Roman") +
      theme(legend.position = "none") +
      labs(title = "Cooccurrences of Nouns & Adjectives", subtitle = "Within Complete Document")
    }
  })
  
  output$coOccuranceAny <- renderPlot({ 
    if (input$cooccurance=='N'){
      return(NULL)
      
    }else{
    annotateData <- datasetInput()
    coocurranceData <- cooccurrence(x = annotateData$lemma)
    wordnetwork <- graph_from_data_frame(head(coocurranceData, 30))
    windowsFonts(Times=windowsFont("Times New Roman"))
    ggraph(wordnetwork, layout = "kk") +
      geom_edge_link(aes(width = cooc, edge_alpha = cooc), edge_colour = "black") +
      geom_node_text(aes(label = name), col = "orange", size = 6) +
      theme_graph(base_family = "Times New Roman") +
      theme(legend.position = "none") +
      labs(title = "Cooccurrences of Any Word", subtitle = "Within Complete Document")
    }
  })
  
})
