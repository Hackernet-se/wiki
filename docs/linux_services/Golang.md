---
title: Golang
permalink: /Golang/
---

[Category:Guider](/Category:Guider "wikilink") **Intro**
Golang är det nya hippa språket som Google har utvecklat. Det är enkelt
att läsa som Python, snabbt och low level som C.

**Golang Concurreny**

So basically goroutines are amazing in go, they are cheap, fast and even
though one might think they run in parallel they don't. So lets say that
I wanna run 2k HTTP GET requests towards skooog.se. Well I can do this
concurrent, but we are gonna run into several issues, one being the
amount of sockets we have on our client machine.

So sockets are expensive, goroutines aren't, this is how we solve it.

``` go
 package main

 import (
    "fmt"
    "io/ioutil"
    "net/http"
    "sync"
 )

 // We need something to recover in case one goroutine fails.
 // Otherwise our whole program might crash or hang

 func cleanup() {
    if r := recover(); r != nil {
        fmt.Println("recovered in cleanup", r)
    }
 }

 func getURL(c chan<- *http.Response, wg *sync.WaitGroup, sem chan bool, url string) {
    defer wg.Done()
    defer cleanup()
    sem <- true
    data, err := http.Get(url)
    if err != nil {
        panic(err)
    }

    c <- data
    <-sem

    // Tell the waitgroup we are done
 }

 func main() {
    // Declare waitgroup
    var wg sync.WaitGroup

    // Make channels with buffersize to fit all our data
    c := make(chan *http.Response, 1000)

    /*
     We create sem to act as a buffer, because goroutines are cheap and we can use a lot, however
     sockets aren't. So we can easily spin up 10000 of goroutines without any issues,
     but then we will start running out of sockets to use.
    */
    sem := make(chan bool, 50)
    for i := 0; i < 1000; i++ {
        // Add 1 to the queue
        wg.Add(1)
        go getURL(c, &wg, sem, "http://skooog.se")
    }
    // Wait until every job we added is done
    wg.Wait()

    // Close channel is needed for when we use the range statement below
    // If we don't close it range will never know when it should stop iterating,
    // this will cause the problem to hang
    close(c)
    fmt.Println("ok")

    httpResponses := [][]byte{}

    for elem := range c {
        content, _ := ioutil.ReadAll(elem.Body)
        //fmt.Println(string(content))
        httpResponses = append(httpResponses, content)
    }

    for _, slice := range httpResponses {
        fmt.Println(string(slice))
    }
 }
```