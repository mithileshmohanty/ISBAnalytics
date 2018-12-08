#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#
# Author : Mithilesh Mohanty

library(shiny)
library(wordcloud2)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  tags$head(tags$style(
    HTML('
           #sidebar {
           background-color: #D3D3D3;
           }
           
           body, label, input, button, select { 
           font-family: "Arial";
           }
           #mainpanel {
           background-color: #DEB887;
           }
             body, label, input, button, select { 
               font-family: "Arial";
             }'  
    )
  )),
  
  # Application title
  titlePanel("NLP using Udpipe"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel( id = "sidebar",
      fileInput("fileText", "Upload Text File (.txt file)"),
      actionButton("checkButton", "Start Process"),
      radioButtons("WordCloud", "Select Word Cloud to show:",
                   c("Noun" = "N",
                     "Verb" = "V",
                     "Both" = "B")),
      radioButtons("cooccurance", "Select cooccurance to show:",
                   c("Noun & Adjectives" = "N",
                     "All Words" = "A",
                       "Both" = "B"))
    ),
    
    # Show a plot of the generated distribution
    mainPanel(id = "mainpanel",
      tabsetPanel(type = "tabs",
                  
                  tabPanel("Overview & App Description",
                           h1(p("Natural Language Processing in R using udpipe demo")),
                           h4(p("Data input")),
                           p("This app supports only text file (.txt) data file. The text file should be in ASCII encoding else the app will not work. For Best result the text corpus should be within 10 MB else theere will be heavy performance hit.",align="justify"),
                           p('Please find the sample text files listed below. Click on the link to download. The app also requires english udpipe text corpus and requisite R packagages. The english udpipe can be downloaded from the link below and should be placed inside the',
                             span(strong(".\\Data\\")),"directory"),
                           
                           a(href="https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics@19e7d67a/TextAnalytics/GroupAssignment-2/Data/DataAnalysis.txt"
                             ,"DataAnalysis.txt"),
                           br(),
                           a(href="https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics@19e7d67a/TextAnalytics/GroupAssignment-2/Data/ISB.txt"
                             ,"Isb.txt"),
                           br(),
                           a(href="https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics@19e7d67a/TextAnalytics/GroupAssignment-2/Data/Nokia.txt"
                             ,"Nokia.txt"),
                           br(),
                           a(href="https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics@19e7d67a/TextAnalytics/GroupAssignment-2/Data/testdata.txt"
                             ,"Testdata.txt"),
                           br(),
                           a(href="https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics@19e7d67a/TextAnalytics/GroupAssignment-2/Data/english-ud-2.0-170801.udpipe"
                             ,"English-ud-2.0-170801.udpipe"),
                           br(),
                           h4('How to use this App'),
                           p('To use this app, click on', 
                             span(strong("Upload text File (.txt file)")),
                             'and uppload a text file(upto 10 MB). Once Text File is uploaded click on Start Process which will prepare the data for your Operations.'),
                           p('Alternatively, You can click on the respective tabs for different operations but it is highly recommended for smoother operations click on Start Process first.'),
                           p('The App offers 3 main functionalities.'),
                           p('',
                           span(strong("Annoted Document")),' It displays the first 100 entries of the annoted document created without the sentence column and provides a way to download the complete annoted document in csv'),
                           p('',
                             span(strong("Word Cloud")),' It displays two word cloud graphs for all the nouns and verbs from the annoted text. On the Right sidebar we have the option to choose which kind of word cloud we want to see Noun, Verb or both'),
                           p('',
                             span(strong("Co-occurrences")),' It displays two two co-occurrences graph for all the words and nouns & Adjectives from the document and displays the same in a network graph. On the right side we have the option to choose between Noun & Ajective or All else Both to create the network Cooccurance graph. '),
                           p(
                             span(strong('Submitted By'))),
                           p(
                             span(strong('Mithilesh Mohanty 11910004'))),
                           p(
                             span(strong('Kiran Krishnakumar 11910053')))
                           ),
                  tabPanel("Annoted Document",
                           dataTableOutput("annotatedDocumentContent"),
                           actionButton("downloadButton", "Download Data As CSV")
                           
                           ),
                  tabPanel("Word Cloud",
                           h3(textOutput("nounCaption")),
                           plotOutput("wordCloudNoun"),
                           h3(textOutput("verbCaption")),
                          plotOutput("wordCloudVerb")
                  ),
                  tabPanel("Co-Occurances",
                           plotOutput("coOccurance",height = "500px",width = "75%"),
                           plotOutput("coOccuranceAny",height = "500px",width = "75%")
                           )
                  
      )
    )
  )
))
