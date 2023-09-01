
def renderTextCenteredAt(text, font, allowed_width): # modified from https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font 
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        if len(line_words) == 1 and font.size(line_words[0])[0] > allowed_width:
            out = []
            line = ''
            for i in line_words[0]:
                fw, fh = font.size(line+'--')
                if fw > allowed_width:
                    out.append(line+'-')
                    line = i
                else:
                    line += i
            #if line != '': out.append(line)
            lines.extend(out)
        lines.append(line)
    return lines
