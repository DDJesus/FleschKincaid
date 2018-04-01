# FleschKincaid

A python library that can analyze bodies of text and return the grade level estimate that an individual would need to complete in order to understand the text. It uses the Flesch Kincaid Grade Level formula to determine the output. You can read more about it here:

https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

I'm working on a way to pip install it or make this easier to use, but currently just place this file in the same directory as the code you are working with and import FleschKincaid.FleschKincaid.

Example:

    > from FleschKincaid import FleschKincaid
    
    > FleschKincaid.grade("This is some sample text.")
    > 1
    > FleschKincaid.grade("In English, grammar is so very important. That is why I have made this fantastic tool!")
    > 4
