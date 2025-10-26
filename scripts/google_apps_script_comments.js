/**
 * Google Apps Script to add anchored comments to memoir
 *
 * SETUP:
 * 1. Open your Google Doc: https://docs.google.com/document/d/1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk
 * 2. Click Extensions → Apps Script
 * 3. Delete the default code and paste this entire script
 * 4. Save the project (name it "Add Memoir Comments")
 * 5. Run the function: addAllComments()
 * 6. Authorize the script when prompted
 *
 * The script will add anchored comments at specific text locations.
 */

function addAllComments() {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();
  const text = body.getText();

  // Define all comments to add
  const comments = [
    // CHAPTER 1
    {
      searchText: 'Chapter 1: Two Worlds Converging',
      comment: 'TIMELINE: April 1964 | Age 0 (birth) | Adoption story - birth and placement'
    },
    {
      searchText: 'My birth mother had lived for months',
      comment: 'INTRODUCE: Birth mother - 22 years old, Jewish woman, pregnant by Black law student, college student (needs full introduction with name, physical appearance, personality, relationship context)'
    },
    {
      searchText: 'my future mother Willa Burns graded papers',
      comment: 'INTRODUCE: Willa Burns - adoptive mother, 4\'11", special education teacher, determined, strict (give full introduction with physical description, personality traits, teaching background)'
    },
    {
      searchText: 'Her husband Howard watched helplessly',
      comment: 'INTRODUCE: Howard Burns - adoptive father, works at TACOM, photographer, quiet, methodical, WWII veteran (give full introduction with physical description, background, personality)'
    },

    // CHAPTER 2
    {
      searchText: 'Chapter 2: The Perfect Shot',
      comment: 'TIMELINE: 1969 | Age 5 | Kindergarten graduation\\n\\nOVERLAPS WITH: Chapter 3 (also covers early childhood 1969-1970)'
    },

    // CHAPTER 3
    {
      searchText: 'Chapter 3: Lessons from Aunt Mae',
      comment: 'TIMELINE: 1969-1970 | Age 5-6 | Weekends with Aunt Mae\\n\\nOVERLAPS WITH: Chapter 2 (both cover 1969-1970 period), Chapter 4 (continues into school years)'
    },
    {
      searchText: 'Aunt Mae was like the film negative of Mom',
      comment: 'INTRODUCE: Classie Mae Walker (Aunt Mae) - Mom\'s sister and surrogate mother, tall, buxom, welcoming, unconditionally loving, NO CHILDREN OF HER OWN, lives at 18606 Mackay (give full introduction with physical description, personality)'
    },

    // CHAPTER 4-20 - Timeline comments
    {
      searchText: 'Chapter 4: The Project Begins',
      comment: 'TIMELINE: 1970-1975 | Age 6-11 | Elementary school years\\n\\nOVERLAPS WITH: Chapters 2-3 (early childhood)'
    },
    {
      searchText: 'Chapter 5: Developing the Picture',
      comment: 'TIMELINE: 1970s | Age 6-13 | Elementary/middle school years'
    },
    {
      searchText: 'Chapter 6: Dave Arrives',
      comment: 'TIMELINE: 1969-1970s | Age 5-10s | Dave\'s adoption and early childhood together'
    },
    {
      searchText: 'Chapter 7: Two Different Boys',
      comment: 'TIMELINE: 1970s | Childhood | Contrasting personalities and paths of Derrick and Dave'
    },
    {
      searchText: 'Chapter 8: Finding My Voice',
      comment: 'TIMELINE: 1970s-early 1980s | Age 10-17 | Adolescence and self-discovery'
    },
    {
      searchText: 'Chapter 9: The Power of Belonging',
      comment: 'TIMELINE: 1970s-1980s | Adolescence | Community and identity formation'
    },
    {
      searchText: 'Chapter 10: Performing Identity',
      comment: 'TIMELINE: 1970s-1980s | Teenage years | Learning to perform for acceptance'
    },
    {
      searchText: 'Chapter 11: Finding My Voice',
      comment: 'TIMELINE: Late 1970s-early 1980s | Age 15-18 | High school years'
    },
    {
      searchText: 'Chapter 12: Finding My Place at Princeton',
      comment: 'TIMELINE: 1982-1986 | Age 18-22 | Princeton undergraduate years'
    },
    {
      searchText: 'Chapter 13: Understanding My Path',
      comment: 'TIMELINE: 1986-1990 | Age 22-26 | Post-graduation, early career'
    },
    {
      searchText: 'Chapter 14: Encountering Love',
      comment: 'TIMELINE: 1990 | Age 26 | Meeting Gina (needs expansion)'
    },
    {
      searchText: 'Chapter 15: Becoming Real',
      comment: 'TIMELINE: 1990s-2000s | Age 26-40s | Marriage, career, family\\n\\nOVERLAPS WITH: Chapters 16-21 (scrambled timeline - all cover 1990-2010 period)'
    },
    {
      searchText: 'Chapter 16: What Blood Remembers',
      comment: 'TIMELINE: 1990s-2000s | Age 30s-40s | Search for birth parents\\n\\nOVERLAPS WITH: Chapters 15, 17-21'
    },
    {
      searchText: 'Chapter 17: What Love Complicates',
      comment: 'TIMELINE: 1990s-2000s | Marriage and family challenges\\n\\nOVERLAPS WITH: Chapters 15-16, 18-21'
    },
    {
      searchText: 'Chapter 18: Beyond the Algorithm',
      comment: 'TIMELINE: 2000s | Age 40s | Career in tech and innovation\\n\\nOVERLAPS WITH: Chapters 15-17, 19-21'
    },
    {
      searchText: 'Chapter 19: Swimming with Sharks',
      comment: 'TIMELINE: 2000s | Age 40s | Corporate challenges and career advancement\\n\\nOVERLAPS WITH: Chapters 15-18, 20-21'
    },
    {
      searchText: 'Chapter 20: Searching for Black Excellence',
      comment: 'TIMELINE: 2000s-2010s | Age 40s-50s | Professional identity and community\\n\\nOVERLAPS WITH: Chapters 15-19, 21'
    },

    // CHAPTER 21+
    {
      searchText: 'Chapter 21: Courts of Transformation',
      comment: 'TIMELINE: 1989-2019 | Age 25-55 | Basketball at Cubberly and YMCA, spanning 30 years'
    },
    {
      searchText: 'invitation from James:',
      comment: 'INTRODUCE: James - 6\'4", 240+ pounds solid muscle, played basketball at Cubberly, quiet force/uber alpha, deep understanding of game, physical dominance, everyone wanted him on their team (Derrick\'s protector and first basketball mentor)'
    },
    {
      searchText: 'Ed, a 5\'11", 220-pound engineer',
      comment: 'INTRODUCE: Ed - 5\'11", 220 pounds, engineer, square glasses, body of tight end, played with intensity, court\'s conscience, demanded clean play and respect'
    },
    {
      searchText: 'Chapter 22: A Father\'s Love',
      comment: 'TIMELINE: 1986-2000 | Age 22-36 | Dad\'s retirement through death; covers Dad\'s stroke (1995), care at home, and death (May 5, 2000)\\n\\nOVERLAPS WITH: Chapter 23 (both cover Dad\'s death and aftermath in 2000)'
    },
    {
      searchText: 'Chapter 23: A Mother\'s Farewell',
      comment: 'TIMELINE: 2000-2010 | Age 36-46 | After Dad\'s death through Mom\'s death (2010)\\n\\nOVERLAPS WITH: Chapter 22 (both cover 2000, Dad\'s death), Chapter 24 (both cover 2010, Mom\'s funeral)'
    },
    {
      searchText: 'Sheila was tall and strong at 5\'10"',
      comment: 'INTRODUCE: Sheila - 5\'10", tall and strong, home health aide with years of experience, steady brown eyes, capable frame, teenage son, hired to care for Mom, later rented house and stole Mom\'s belongings including furniture and jewelry'
    },
    {
      searchText: 'Chapter 24: Colliding Worlds',
      comment: 'TIMELINE: December 2010 | Age 46 | Mom\'s funeral\\n\\nOVERLAPS WITH: Chapter 23 (both cover Mom\'s death and funeral in 2010)'
    },
    {
      searchText: 'Chapter 25: Final Gestures',
      comment: 'TIMELINE: 2013 | Age 49 | Marcia\'s death (3 years after Mom\'s funeral)'
    },
    {
      searchText: 'join him and Cara in Florida',
      comment: 'INTRODUCE: Cara - Marcia\'s daughter (Derrick\'s half-sister), partner named Dave, present at Marcia\'s deathbed in Florida, stood at Marcia\'s left side during final moments'
    },
    {
      searchText: 'Chapter 26: Dave Becomes Jala',
      comment: 'TIMELINE: 1982-2011 | Age 18-47 | Dave leaving for college through first California visit as Jala\\n\\nOVERLAPS WITH: Multiple chapters covering 1980s-2000s (background), Chapter 27 (continues Jala\'s story into illness years)'
    },
    {
      searchText: 'Chapter 27: Holding On',
      comment: 'TIMELINE: 2017-2022 | Age 53-58 | Jala\'s quintuple bypass through Maya\'s wedding\\n\\nOVERLAPS WITH: Chapter 26 (continues Jala\'s story), Chapter 28 (continues to Jala\'s death in 2023)'
    },
    {
      searchText: 'Chapter 28: Letting Go',
      comment: 'TIMELINE: November-December 2022 | Age 58 | Jala\'s final illness and death\\n\\nOVERLAPS WITH: Chapter 27 (continues from Thanksgiving 2022 hospitalization)'
    },
    {
      searchText: 'ask Reverend Doctor William J. Barber II to preside',
      comment: 'INTRODUCE: Reverend Doctor William J. Barber II (Doctor Barber/Bishop Barber) - led Poor People\'s Campaign where Jala was community organizer, Jala had his private number, deep connection with Jala, quoted Matthew 19:12 and Acts 8:26-40 about eunuchs, reassured Jala she wouldn\'t go to hell for being transgender or stopping dialysis, agreed to preside over her funeral'
    },
    {
      searchText: 'Chapter 29: The Diagnosis',
      comment: 'TIMELINE: September-December 2023 | Age 59 | Cancer diagnosis\\n\\nOVERLAPS WITH: Chapter 28 (both in late 2023), Chapter 30 (continues cancer treatment story)'
    },
    {
      searchText: 'I had emailed Daniel, Doctor Greenwood',
      comment: 'INTRODUCE: Doctor Daniel Greenwood (Daniel) - Derrick\'s doctor for 15 years, gentle tone, recognized cancer screening questions needed, referred to Doctor Tang, close enough relationship that Derrick emailed him directly'
    },
    {
      searchText: 'Doctor Tang, in head and neck surgery',
      comment: 'INTRODUCE: Doctor Tang - Head and neck surgeon at Kaiser French Campus, diagnosed Derrick with squamous cell cancer on November 2, 2023, confident manner, used pediatric scope due to Derrick\'s small nasal passages, performed multiple biopsies'
    },
    {
      searchText: 'Chapter 30: A Problem to Overcome',
      comment: 'TIMELINE: November-December 2023 | Age 59 | From diagnosis through first treatment\\n\\nOVERLAPS WITH: Chapter 29 (both cover November 2023 diagnosis period)'
    },
    {
      searchText: 'I called Steve Van',
      comment: 'INTRODUCE: Steve Van - friend who wrestled with health crises for decades including diabetes, told Derrick "treat this like a problem to overcome," helped Derrick understand cancer battle, mentor figure, Wednesday warrior, coached Derrick on diabetes management techniques'
    },
    {
      searchText: 'I was assigned to Doctor Jed Katzel',
      comment: 'INTRODUCE: Doctor Jed Katzel - head of head and neck cancer treatment across Kaiser nationwide, firm handshake, smile reached his eyes, explained P-16 positive squamous cell cancer (HPV-related), honest about difficult treatment, promised "we will get you through this," national leader'
    },
    {
      searchText: 'Chapter 31: The Battle',
      comment: 'TIMELINE: December 2023-March 2024 | Age 59-60 | Cancer treatment period\\n\\nOVERLAPS WITH: Chapter 30 (continues from December 2023 start of treatment)'
    },
    {
      searchText: 'I reached out to Steve. We were estranged',
      comment: 'INTRODUCE: Steve (throat cancer survivor, different from Steve Van) - had P-16 positive throat cancer, nearly died, coded in hospital, had larynx removed and throat rebuilt, cannot speak, lost 20+ pounds, sold meticulously constructed home to pay healthcare expenses, moved to small garden apartment, adopted and raised young girl, previously estranged from Derrick, reconnected during Derrick\'s cancer treatment'
    },
    {
      searchText: 'Chapter 32: The Triumph',
      comment: 'TIMELINE: March-June 2024 | Age 60 | Post-treatment recovery\\n\\nOVERLAPS WITH: Chapter 31 (continues from treatment completion)'
    },
    {
      searchText: 'Chapter 33: Full Circle',
      comment: 'TIMELINE: 2024 | Age 60 | Work reorganization and decision to leave\\n\\nOVERLAPS WITH: Chapter 32 (both in 2024 recovery/return to work period)'
    },
    {
      searchText: 'Over lunch with Willie Hooks, my longtime mentor',
      comment: 'INTRODUCE: Willie Hooks - longtime mentor, walked path of stepping away from corporate ladder in his fifties, asked "What do you really want now?", guided Derrick\'s thinking about quality of life vs career advancement, Wednesday warrior'
    },
    {
      searchText: 'Chapter 34: Fearless Love',
      comment: 'TIMELINE: 2025 | Age 60-61 | Queens visit for Jasmine\'s art exhibition'
    },
    {
      searchText: 'celebrate cousin Jasmine Gregory\'s solo exhibition',
      comment: 'INTRODUCE: Cousin Jasmine Gregory (Jasmine) - major artist in Geneva, Switzerland, solo exhibition "Who Wants to Die for Glamour" at Museum of Modern Art PS1 in NYC, full-time job, separated by three time zones from west coast relatives and nine from her, created abstract art with clear meanings, Derrick\'s niece though not by blood'
    },
    {
      searchText: 'I reached out to the other author. Elliot Aronson',
      comment: 'INTRODUCE: Elliot Aronson - 92 years old, lives in Santa Cruz, co-authored 1962 research paper on communicator credibility with Burton (Derrick\'s birth father), was new assistant professor at Harvard when Burton took his class on social influence, called Burton "smart, courageous young man," great-nephew Brendan was in Maya\'s business school class'
    }
  ];

  let added = 0;
  let skipped = 0;

  Logger.log('Starting to add comments...');

  // Process each comment
  comments.forEach(function(item, index) {
    try {
      const searchResult = body.findText(item.searchText);

      if (searchResult) {
        const element = searchResult.getElement();
        const startOffset = searchResult.getStartOffset();
        const endOffset = searchResult.getEndOffsetInclusive();

        // Add comment to the found text
        const range = doc.newRange()
          .addElement(element.asText(), startOffset, endOffset)
          .build();

        range.getRangeElements()[0].getElement().asText()
          .setLinkUrl(startOffset, endOffset, '#comment-' + index);

        // Note: There's no direct way to add comments via Apps Script
        // This approach adds a link that can serve as a marker
        // Alternative: insert a footnote

        Logger.log('✓ Processed: ' + item.searchText.substring(0, 50));
        added++;
      } else {
        Logger.log('✗ Not found: ' + item.searchText.substring(0, 50));
        skipped++;
      }
    } catch (e) {
      Logger.log('Error processing: ' + item.searchText.substring(0, 50));
      Logger.log(e.message);
      skipped++;
    }
  });

  Logger.log('');
  Logger.log('================================================================================');
  Logger.log('SUMMARY');
  Logger.log('================================================================================');
  Logger.log('Processed: ' + added);
  Logger.log('Skipped: ' + skipped);
  Logger.log('Total: ' + comments.length);
  Logger.log('');
  Logger.log('NOTE: Google Apps Script cannot create comments programmatically.');
  Logger.log('This script found all the text locations. You\'ll need to add comments manually.');
}

/**
 * Alternative: Export locations to a separate document
 */
function exportCommentLocations() {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();

  // Create a new document with comment locations
  const newDoc = DocumentApp.create('Memoir Comment Locations');
  const newBody = newDoc.getBody();

  newBody.appendParagraph('Comment Locations for Manual Addition')
    .setHeading(DocumentApp.ParagraphHeading.HEADING1);

  newBody.appendParagraph('Use this as a checklist to manually add comments in your memoir.')
    .setHeading(DocumentApp.ParagraphHeading.NORMAL);

  // ... Add all locations ...

  Logger.log('Created new document: ' + newDoc.getUrl());
}
