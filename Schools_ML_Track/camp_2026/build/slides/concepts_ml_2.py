"""Machine Learning concept slides, sessions 13 to 24, labs F03 and F04 and the extension ML25."""
CONCEPTS = {13: {'question': {'fig': 'ml_features_target',
                   'alt': 'A table of homes with feature columns and a hidden target column, feeding a model that guesses the rent',
                   'say': 'Look at the table. The first two columns, area and rooms, are the features. They are what the model is allowed to see. '
                          'The last column, the rent, is the target. It is the answer we want. The model sees the features and guesses the rent. '
                          'Today we ask what the session one model learned from, and how well a plain guess would have done without any model at '
                          'all.'},
      'word_icons': {'feature': ('ml_icon', {'kind': 'grid_col'}),
                     'training data': ('ml_r4_icon', {'kind': 'tr_table'}),
                     'test data': ('ml_r4_icon', {'kind': 'te_table'}),
                     'leakage': ('ml_r4_icon', {'kind': 'leak'}),
                     'baseline': ('ml_icon', {'kind': 'flat'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A baseline is the plain guess every model must beat',
                  'fig': 'ml_baseline_guess',
                  'points': ['Always guess the mean of the training rents.', 'No model is used.', 'Beat this or the model adds nothing.'],
                  'say': 'Before we trust a model, we try the laziest guess possible. Guess the same number for every home, the average rent of the '
                         'training homes. That is the baseline.\n'
                         '\n'
                         'If a model cannot do better than this plain guess, it has learned nothing useful. How wrong do you expect the plain guess '
                         'to be?'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Practice and exam questions must be different',
                  'fig': 'ml_practice_vs_exam',
                  'points': ['Training data is the practice.', 'Test data is the exam.', 'A model must never practise on the exam.'],
                  'say': 'A student who has seen the exam questions in advance scores well and proves nothing. A model is the same. It learns from '
                         'the training data. We check it on test data it has never seen.\n'
                         '\n'
                         'Why would a perfect score on the practice questions not tell us much?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The learned line rises as the area grows',
                  'fig': 'ml_open_model',
                  'points': ['Each dot is one home.', 'The line is what the model learned.', 'It is a rule that stands in for the list of homes.'],
                  'say': 'Open the session one model and look inside. It is a line through the homes. Give it an area and it reads off a rent. It '
                         'keeps a rule instead of a list of the homes it saw.\n'
                         '\n'
                         'Point to where a fifty square metre home would land on the line.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A feature must exist before the answer does',
                  'fig': 'ml_leakage_timeline',
                  'points': ['Area is known before the rent is set.',
                             'Information from after the rent is leakage.',
                             'Leakage makes a model look too good.'],
                  'say': 'A feature is only fair if we would have it before we need the answer. The area of a home is known before the rent is set. '
                         'A figure written down after the rent was agreed is information from the future.\n'
                         '\n'
                         'Using such a column is called leakage. It makes a model look brilliant on paper and useless in real life.'}]},
 14: {'question': {'fig': 'ml_eight_homes_lines',
                   'alt': 'Eight homes with a hand-drawn line, a fitted line and a flat mean line, with their average misses',
                   'say': 'Eight homes, three lines. The dashed red line is my own guess and it misses by about fifty six thousand shillings on '
                          'average. The grey flat line is the mean for every home, and it misses by about one hundred and nine thousand. The black '
                          'line is the one the computer fitted, and it misses by about twenty thousand. Today we find out how a straight line is '
                          'judged and how a computer finds a better one than we can by eye.'},
      'word_icons': {'regression': ('ml_icon', {'kind': 'line'}),
                     'slope': ('ml_r4_icon', {'kind': 'rise'}),
                     'intercept': ('ml_r4_icon', {'kind': 'intercept'}),
                     'fit': ('ml_r4_icon', {'kind': 'fit_arrow'}),
                     'predict': ('ml_r4_icon', {'kind': 'predict'}),
                     'error': ('ml_r4_icon', {'kind': 'gap'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A line has a start and a rise per square metre',
                  'fig': 'ml_line_anatomy',
                  'points': ['The intercept is the start at area zero.',
                             'The slope is the rise for each extra square metre.',
                             'Rent equals start plus slope times area.'],
                  'say': 'A straight line is described by two numbers. The intercept is where the line starts when the area is zero. The slope is '
                         'how much the rent rises for every extra square metre.\n'
                         '\n'
                         'To predict a rent, take the start, then add the slope times the area. Try it for a home of fifty square metres on paper.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'An error is the gap between line and real rent',
                  'fig': 'ml_guess_gaps',
                  'points': ['Each black bar is one miss.', 'Ignore whether it is above or below.', 'The average of the bars is the score.'],
                  'say': 'For each home we measure how far the line is from the real rent. Those gaps are the errors, drawn here as bars. We ignore '
                         'whether the line was too high or too low and look only at the size.\n'
                         '\n'
                         'The average of the bars is one number that scores the whole line. A smaller number means a better line.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'The fitted line beats my guess and the flat mean',
                  'fig': 'ml_three_lines',
                  'points': ['Always the mean: 109,399.', 'My hand line: 56,282.', 'The fitted line: 20,077.'],
                  'say': 'Here are the three scores side by side. The plain mean guess misses by about a hundred and nine thousand shillings. My '
                         'hand drawn line misses by about fifty six thousand. The fitted line misses by about twenty thousand.\n'
                         '\n'
                         'The computer tries many lines and keeps the one with the smallest average miss.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Fit learns the line and predict reads a new answer',
                  'fig': 'ml_fit_predict_flow',
                  'points': ['Fit takes inputs and answers together.', 'The result is a learned line.', 'Predict gives a guess for a new input.'],
                  'say': 'There are two steps. Fit shows the model examples, each with its inputs and its true answer, and the model learns a line. '
                         'Predict gives the learned line a new input, with no answer, and gets a guess back.\n'
                         '\n'
                         'Fit is learning. Predict is using what was learned.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A line is trustworthy near its examples only',
                  'fig': 'ml_extrapolation',
                  'points': ['Examples live in one region.', 'Far from them there is no evidence.', 'Ask for predictions inside the data.'],
                  'say': 'A line is drawn from the homes we have. Ask it about a home far outside that range and it still gives an answer, but '
                         'nothing backs it up.\n'
                         '\n'
                         'A number of ten thousand square metres is easy to type and meaningless to trust. Stay inside the range of your '
                         'examples.'}]},
 15: {'question': {'fig': 'ml_split_homes',
                   'alt': 'One hundred and twenty homes as squares, ninety for training and thirty gold ones for testing',
                   'say': 'Each square is one of our one hundred and twenty homes. Ninety of them, the white squares, are for training. The thirty '
                          'gold squares are for testing, and the model never sees them while it learns. A shuffle chose the gold squares, which is '
                          'why they are spread out. Today the question is whether the rent model beats a plain guess on homes it has never seen.'},
      'word_icons': {'train and test split': ('ml_icon', {'kind': 'split'}),
                     'held-out records': ('ml_r4_icon', {'kind': 'held_out'}),
                     'test_size': ('ml_r4_icon', {'kind': 'pie_small'}),
                     'random_state': ('ml_icon', {'kind': 'die'}),
                     'baseline model': ('ml_icon', {'kind': 'flat'}),
                     'mean absolute error': ('ml_r4_icon', {'kind': 'mae'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Shuffle first, then cut, for a fair test sample',
                  'fig': 'ml_shuffle_cut',
                  'points': ['The file is in order of home number.', 'Shuffle with random_state 7.', 'Cut after 30 for the test part.'],
                  'say': 'The homes in the file are in order. If we cut the file in the middle, one part might hold all the small homes. So we '
                         'shuffle first, then cut off thirty homes for the test.\n'
                         '\n'
                         'A random state of seven makes the shuffle the same every time, so your result matches mine.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Four names catch the four pieces the split returns',
                  'fig': 'ml_four_names',
                  'points': ['Training inputs and training answers.', 'Test inputs and test answers.', 'The order matters.'],
                  'say': 'The split hands back four pieces: the training inputs, the test inputs, the training answers and the test answers. You '
                         'catch them in four names on the left of the equals sign, in that order.\n'
                         '\n'
                         'Swap two names and your code runs, but it quietly learns from the wrong thing. Check the order every time.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The plain guess misses by about 110,000 shillings',
                  'fig': 'ml_mae_test_baseline',
                  'points': ['Guess the training mean for each test home.', 'Measure the average miss.', 'The baseline misses by 110,169.'],
                  'say': 'First we score the plain guess. Take the mean rent of the training homes, guess it for each of the thirty test homes, and '
                         'average the misses. The answer is about one hundred and ten thousand shillings.\n'
                         '\n'
                         'That is the number the model has to beat.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The fitted model misses by about 12,000 shillings',
                  'fig': 'ml_mae_test_model',
                  'points': ['Same thirty test homes.', 'The model misses by 11,889.', 'About nine times closer than the plain guess.'],
                  'say': 'Now the model. It learned from the ninety training homes and has never seen the thirty test homes. Its average miss is '
                         'about eleven thousand eight hundred and eighty nine shillings.\n'
                         '\n'
                         'Compared with a hundred and ten thousand for the plain guess, that is roughly nine times closer.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Ten shuffles give ten slightly different scores',
                  'fig': 'ml_seed_dice',
                  'points': ['Each shuffle picks different test homes.', 'The scores stay in the same region.', 'Report the seed you used.'],
                  'say': 'Change the random state and a different set of homes lands in the test part, so the score changes a little. Ten shuffles '
                         'give ten nearby numbers.\n'
                         '\n'
                         'That is why we report which seed we used, and why we should be careful about reading too much into small differences.'}]},
 16: {'question': {'fig': 'ml_tree_diagram',
                   'alt': 'A decision tree for iris flowers with two questions and three species at the leaves',
                   'say': 'Here is a small decision tree. It asks one question about the petal length. If the petal is short, the flower is a '
                          'setosa. If not, it asks a second question about the petal width and decides between versicolor and virginica. A tree is a '
                          'set of questions with yes or no answers. Today we write our own rule for the flowers, let a computer learn its own tree, '
                          'and see which one does better.'},
      'word_icons': {'classification': ('ml_r4_icon', {'kind': 'classes'}),
                     'decision tree': ('ml_icon', {'kind': 'tree'}),
                     'class label': ('ml_r4_icon', {'kind': 'tag_label'}),
                     'accuracy': ('ml_r4_icon', {'kind': 'ratio'}),
                     'majority baseline': ('ml_r4_icon', {'kind': 'majority'}),
                     'depth': ('ml_r4_icon', {'kind': 'depth'})},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Species overlap in petal length, so one cut fails',
                  'fig': 'ml_petal_ranges',
                  'points': ['Setosa is clearly small.', 'Versicolor and virginica overlap.', 'A good rule needs two cuts.'],
                  'say': 'Look at the range of petal lengths for each species. Setosa sits alone at the small end. Versicolor and virginica overlap '
                         'in the middle. A single cut cannot separate all three.\n'
                         '\n'
                         'Where would you place your two cuts?'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Accuracy counts right answers out of all answers',
                  'fig': 'ml_accuracy_tokens',
                  'points': ['Nine right out of ten.', 'Nine divided by ten is 0.9.', 'As a percentage, that is 90.'],
                  'say': 'Accuracy is easy. Count how many answers were right, and divide by how many answers there were. Nine out of ten gives zero '
                         'point nine, which is ninety percent.\n'
                         '\n'
                         'It is the same proportion idea you used on the shop sales.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'My hand rule cuts the flowers into three zones',
                  'fig': 'ml_zones_hand',
                  'points': ['Two cuts on petal length.', 'Each zone gets one species.', 'Mistakes sit where the species overlap.'],
                  'say': 'My own rule makes two cuts on the petal length and gives each zone one species. It is simple to explain. Wrong answers '
                         'hide where two species overlap.\n'
                         '\n'
                         'On all one hundred and fifty flowers this rule is wrong seven times, an accuracy of zero point nine five three.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The tree cuts on length and on width',
                  'fig': 'ml_zones_tree',
                  'points': ['One cut on length, one on width.', 'The zones are boxes.', 'The computer chose the cuts itself.'],
                  'say': 'The tree also makes two cuts, but one is on petal length and one is on petal width. The computer searched for cuts that '
                         'separate the species best.\n'
                         '\n'
                         'This tree was fitted on all one hundred and fifty flowers and is wrong six times, an accuracy of zero point nine six. Where does it do better than my rule?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The model returns codes that we translate to names',
                  'fig': 'ml_codes_names',
                  'points': ['The model works with codes 0, 1 and 2.', 'A code is only a name tag.', 'Translate it back to a species.'],
                  'say': 'Inside the model each species has a number: zero, one or two. The numbers are only name tags. Two is not bigger than zero '
                         'in any useful sense.\n'
                         '\n'
                         'When you read results, translate the codes back into species names so that other people can follow.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Guessing one species is right one time in three',
                  'fig': 'ml_majority_baseline',
                  'points': ['Three species are equally common.', 'Guess setosa every time.', 'Accuracy is about 0.33.'],
                  'say': 'The three species are equally common, so a plain guess of one species is right about one time in three. Any tree has to '
                         'beat that to be worth using.\n'
                         '\n'
                         'A score of seventy percent sounds good, but it only means something when we know what a lazy guess would have scored.'}]},
 17: {'question': {'fig': 'ml_overfit_curve',
                   'alt': 'A wiggly curve through eight training trips misses new trips badly while a plain line misses them far less',
                   'say': 'The gold dots are eight training trips. The red curve passes through every one of them, so on training data it misses by '
                          'nothing at all. The white dots are trips it has never seen, and there the red curve misses by more than nine thousand '
                          'shillings. The plain black line is much better, at about two and a half thousand. Today we learn why a very high score is '
                          'sometimes a warning sign.'},
      'word_icons': {'overfitting': ('ml_r4_icon', {'kind': 'wiggle'}),
                     'confusion matrix': ('ml_icon', {'kind': 'matrix'}),
                     'actual and predicted': ('ml_r4_icon', {'kind': 'pair_marks'}),
                     'validation records': ('ml_r4_icon', {'kind': 'three_way'}),
                     'final test': ('ml_icon', {'kind': 'lock'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A confusion matrix shows where the answers went',
                  'fig': 'ml_confusion_toy',
                  'points': ['Rows are what was true.', 'Columns are what we said.', 'The diagonal holds the right answers.'],
                  'say': 'Accuracy is one number. A confusion matrix shows the detail. Each row is what was true. Each column is what we said. The '
                         'diagonal, from top left to bottom right, holds the answers we got right.\n'
                         '\n'
                         'In this small example three answers are on the diagonal and two are off it.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Read one answer at a time to find its cell',
                  'fig': 'ml_confusion_reading',
                  'points': ['Find the row for what was true.', 'Find the column for what we said.', 'The answer lands where they meet.'],
                  'say': 'To place an answer, find the row for the truth and the column for what we said. The two meet in one cell.\n'
                         '\n'
                         'Answer two was no, and we said yes. Go along the row for no, down the column for yes, and put a mark where they cross.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A model that bends more memorises the practice',
                  'fig': 'ml_complexity_gap',
                  'points': ['Gold bars show the training miss.', 'White bars show the miss on new trips.', 'The gap grows as the curve bends.'],
                  'say': 'Allow the line to bend more, and the miss on training trips shrinks. The miss on new trips grows. The model is memorising '
                         'the practice and failing the exam.\n'
                         '\n'
                         'The same thing happens to a tree that is allowed too many questions.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Peeking at the final test turns it into practice',
                  'fig': 'ml_peek_test',
                  'points': ['Score on the final test.', 'Change a setting and score again.', 'The test now shapes your choice.'],
                  'say': 'It is tempting to check the final test, change a setting, and check again. Each peek leaks a little of the test into your '
                         'decisions, and the test stops being a fair exam.\n'
                         '\n'
                         'So we keep a separate validation part for choosing settings, and we open the final test once.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Choose on validation and open the final test last',
                  'fig': 'ml_three_way_bar',
                  'points': ['Train on 90.', 'Choose a setting using the 30 validation flowers.', 'Open the 30 test flowers once.'],
                  'say': 'The flowers are split three ways. Ninety for training. Thirty for validation, where we compare settings. Thirty for the '
                         'final test, which stays locked until the very end.\n'
                         '\n'
                         'Next session you will do this yourself and compare two tree depths.'}]},
 18: {'question': {'fig': 'ml_choose_freeze_test',
                   'alt': 'Three candidate models scored on validation, the best one frozen, then tested once and reported',
                   'say': 'This is the order of work for checkpoint two. Score the baseline and two trees on the validation flowers. Pick the best. '
                          'Freeze it, so nothing changes any more. Test it once on the locked flowers and report the number. The choice is made '
                          'before the test is ever opened.'},
      'word_icons': {'stratify': ('ml_r4_icon', {'kind': 'strata'}),
                     'validation score': ('ml_r4_icon', {'kind': 'bars_pick'}),
                     'frozen choice': ('ml_r4_icon', {'kind': 'snow'}),
                     'split sizes': ('ml_r4_icon', {'kind': 'three_way'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Two cuts turn 150 flowers into 90, 30 and 30',
                  'fig': 'ml_two_cuts',
                  'points': ['First cut: 30 flowers go to the final test.',
                             'Second cut: 30 of the 120 go to validation.',
                             'The rest, 90, is for training.'],
                  'say': 'Start with all one hundred and fifty flowers. The first cut sets aside thirty for the final test. That leaves a hundred '
                         'and twenty. The second cut takes thirty of those for validation. Ninety are left for training.\n'
                         '\n'
                         'Check that your three sizes add up to a hundred and fifty.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Stratify keeps the same species mix in every part',
                  'fig': 'ml_stratify',
                  'points': ['Each part holds all three species.', 'The shares match the whole set.', 'A small part cannot miss a species.'],
                  'say': 'A plain shuffle can leave a small part without one of the species by bad luck. Stratify prevents that. Every part gets '
                         'each species in the same share as the whole.\n'
                         '\n'
                         'In this picture each part has the same proportion of the three species.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The final test has ten flowers of each species',
                  'fig': 'ml_confusion_3x3',
                  'points': ['Each row adds up to ten.', 'The diagonal holds right answers.', 'Off the diagonal are the mix-ups.'],
                  'say': 'The final test holds thirty flowers, ten of each species, so every row of the confusion matrix adds up to ten. The '
                         'diagonal cells are the flowers we named correctly. Anything off the diagonal is a mix-up between two species.\n'
                         '\n'
                         'Your own matrix will have real numbers in these cells.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Checkpoint two needs seven pieces of evidence',
                  'fig': 'ml_checkpoint_two_list',
                  'points': ['Report validation and final test apart.'],
                  'say': 'Before you hand in checkpoint two, tick these seven items. The three split sizes, the baseline score, two validation '
                         'scores, the chosen depth, the final test accuracy, the confusion matrix and two limitations.\n'
                         '\n'
                         'All of them must come from one notebook that you restarted and ran from the top.'}]},
 19: {'question': {'fig': 'ml_three_datasets',
                   'alt': 'Three datasets: homes, boda-boda fares and iris flowers, each with inputs and a target',
                   'say': 'You have met three datasets. The homes file has a hundred and twenty homes and its target is the rent, a number. The '
                          'fares file has a hundred and fifty boda-boda trips and its target is the fare, also a number. The iris file has a hundred '
                          'and fifty flowers and its target is the species, a category. For your project you pick the one you can answer with a fair '
                          'test in two weeks.'},
      'word_icons': {'project plan': ('ml_r4_icon', {'kind': 'checklist'}),
                     'leakage column': ('ml_r4_icon', {'kind': 'leak'}),
                     'inputs': ('ml_icon', {'kind': 'grid_col'}),
                     'limits': ('ml_r4_icon', {'kind': 'bounds'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Only columns known at booking can be inputs',
                  'fig': 'ml_trip_timeline',
                  'points': ['Distance, rush hour and rain are known at booking.',
                             'The fare is known when the ride ends.',
                             'The tip comes after, so it leaks.'],
                  'say': 'Follow a boda-boda trip in time. At booking we know the distance, whether it is rush hour and whether it is raining. When '
                         'the ride ends we know the fare. Afterwards, maybe, comes a tip.\n'
                         '\n'
                         'The tip is known too late to help predict the fare, so it must stay out of the inputs.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'The tip tracks the fare most closely: a warning',
                  'fig': 'ml_fares_correlation',
                  'points': ['The tip has the highest correlation, 0.88.', 'Distance follows at 0.76.', 'A strong link does not make a column fair.'],
                  'say': 'Correlation measures how closely two columns move together. The tip moves most closely with the fare, at zero point eight '
                         'eight. Distance is next, at zero point seven six.\n'
                         '\n'
                         'A high number tempts us to use the tip. But the tip is only known after the trip, so using it would be cheating.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A safe project question fits two weeks',
                  'fig': 'ml_plan_sizes',
                  'points': ['Choose a question with data behind it.',
                             'The answer should be a number or a label.',
                             'Avoid questions about everything.'],
                  'say': 'On the left is a question that fits two weeks. Can distance and rush hour predict a boda-boda fare? There is data, and the '
                         'answer is a number. On the right is a question that is far too big. Nothing in our files can answer it.\n'
                         '\n'
                         'Test your own question against these two cards.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A project plan has seven headings',
                  'fig': 'ml_plan_storyboard',
                  'points': ['Write each heading before any code.'],
                  'say': 'Your plan has seven headings: the question, the dataset, the target, the inputs, the baseline, the evaluation and the '
                         'limits. Fill them in before you write a single line of code.\n'
                         '\n'
                         'The plan keeps you honest. When the results arrive, you cannot quietly change the question to fit them.'}]},
 20: {'question': {'fig': 'ml_fare_baseline_gaps',
                   'alt': 'Thirty validation trips with a flat line at the training mean and bars showing each miss, average 4,361 shillings',
                   'say': 'The red flat line is the plain guess: the mean fare of the training trips, about nine thousand two hundred and seventy '
                          'one shillings. Each black bar is how far one validation trip is from that line. Their average is four thousand three '
                          'hundred and sixty one shillings. That is the bar every model has to beat. Today you work it out for your own project.'},
      'word_icons': {'three-way split': ('ml_r4_icon', {'kind': 'three_way'}),
                     'baseline error': ('ml_icon', {'kind': 'flat'}),
                     'scatter plot': ('ml_icon', {'kind': 'dots'}),
                     'training only': ('ml_r4_icon', {'kind': 'tr_table'})},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'The fares split into 90, 30 and 30 trips',
                  'fig': 'ml_three_way_bar_fares',
                  'points': ['Same shape as the flowers split.', 'Training teaches.', 'Test stays locked.'],
                  'say': 'The fares file is cut the same way as the flowers. Ninety trips to learn from, thirty to choose between models, and thirty '
                         'locked away for the end.\n'
                         '\n'
                         'Use the same random state as before so your numbers match the ones on the screen.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'The baseline mean uses the training trips only',
                  'fig': 'ml_train_only_mean',
                  'points': ['Take the mean of the 90 training fares.', 'Never include validation or test trips.', 'Otherwise the guess has peeked.'],
                  'say': 'The baseline is the mean fare of the training trips. If you take the mean of all hundred and fifty, the guess has already '
                         'seen the test trips and its score is a little too good.\n'
                         '\n'
                         'Check which table your mean comes from.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Each dot in a scatter plot is one trip',
                  'fig': 'ml_scatter_read',
                  'points': ['Distance runs across.', 'Fare runs up.', 'The gold dot is one trip.'],
                  'say': 'A scatter plot gives every trip a dot. The distance is how far across the dot sits. The fare is how high it sits. The gold '
                         'dot is one trip of about eleven point six kilometres that cost fourteen thousand eight hundred shillings.\n'
                         '\n'
                         'Find a trip of about two kilometres. What did it cost?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Longer trips cost more, correlation near 0.76',
                  'fig': 'ml_fare_scatter',
                  'points': ['The dots climb to the right.', 'The red line follows them.', 'Correlation 0.76 means a strong link.'],
                  'say': 'Draw the ninety training trips and the dots climb to the right. Longer rides cost more. A straight line follows them, and '
                         'the correlation is about zero point seven six.\n'
                         '\n'
                         'That strong link is why distance is a promising input.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A model must score below the plain guess',
                  'fig': 'ml_bar_to_beat',
                  'points': ['Validation miss for the plain guess: 4,361 UGX.'],
                  'say': 'This is the bar. The plain guess misses by four thousand three hundred and sixty one shillings on the validation trips. '
                         'Every model you try next session has to land to the left of it.\n'
                         '\n'
                         'A model that cannot beat the bar is not helping, however clever it sounds.'}]},
 21: {'question': {'fig': 'ml_fair_bars',
                   'alt': 'Validation errors of a plain guess, distance only, distance with rush hour and rain, and a model that uses the tip',
                   'say': 'Four bars. The plain guess misses by four thousand three hundred and sixty one shillings. Using distance alone brings it '
                          'to two thousand four hundred and fifteen. Adding rush hour and rain brings it to two thousand two hundred and fifty five. '
                          'The last bar, which uses the tip, is much shorter, but that model is not allowed. Today you compare candidates fairly and '
                          'defend every input.'},
      'word_icons': {'fair comparison': ('ml_r4_icon', {'kind': 'balance'}),
                     'candidate model': ('ml_icon', {'kind': 'line'}),
                     'validation error': ('ml_r4_icon', {'kind': 'gap'}),
                     'coding assistant': ('ml_r4_icon', {'kind': 'code'}),
                     'AI use log': ('ml_r4_icon', {'kind': 'checklist'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Fair comparison: same trips for every model',
                  'fig': 'ml_same_split',
                  'points': ['Same 30 validation trips.', 'Same error measure.', 'Then the scores can be compared.'],
                  'say': 'If two models are scored on different trips, a difference in score might come from the trips rather than the models. So '
                         'every candidate is scored on the same thirty validation trips, with the same error measure.\n'
                         '\n'
                         'Then, and only then, a lower number really means a better model.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Ask of every input: known before the answer?',
                  'fig': 'ml_inputs_known',
                  'points': ['Distance, rush hour and rain pass.', 'The tip fails.', 'Failing inputs stay out, however good the score.'],
                  'say': 'For each input ask one question. Did we know it before the fare was set? Distance, rush hour and rain pass. The tip fails, '
                         'because it exists only after the trip.\n'
                         '\n'
                         'The tip makes the score look wonderful, and that is exactly why it is dangerous.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A coding assistant gives plausible code to test',
                  'fig': 'ml_assistant_loop',
                  'points': ['Predict what the hint does.', 'Run it and test it.', 'Keep or reject it and log the choice.'],
                  'say': 'A coding assistant can suggest code quickly. Its answers sound sure of themselves, and some are wrong. Treat each '
                         'suggestion as a hint. Predict what it does, run it, test it with a check, then keep it or throw it away and note what you '
                         'did.\n'
                         '\n'
                         'A plausible answer is not a checked answer.'},
                 {'at': 1,
                  'kind': 'pair',
                  'title': 'Code that adds instead of multiplying looks fine',
                  'figs': [('ml_total_bug', {'side': 'plus'}), ('ml_total_bug', {'side': 'times'})],
                  'captions': ['The suggested code adds price and quantity: 2003.', 'The fixed code multiplies them: 6000.'],
                  'say': 'Here is a suggestion that looks fine at first glance. The function is meant to give the total for three items at two '
                         'thousand shillings each. It adds the numbers and returns two thousand and three.\n'
                         '\n'
                         'One test with numbers you can work out in your head would have caught it. Run a check before you trust the code.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A decision card records what you kept and why',
                  'fig': 'ml_decision_card',
                  'points': ['Name the inputs you keep.', 'Give the validation error.', 'State what you left out and why.'],
                  'say': 'Finish with a decision card. It says which inputs you keep, how well they did on validation compared with the plain guess, '
                         'and which input you left out and why.\n'
                         '\n'
                         'If you can write the card in three lines, you understand your own project.'}]},
 22: {'question': {'fig': 'ml_final_test_bars',
                   'alt': 'Final test errors for the plain guess, 3,617 shillings, and the frozen model, 2,936 shillings',
                   'say': 'Here is the answer to the question for today. On the thirty locked trips, the plain guess misses by three thousand six '
                          'hundred and seventeen shillings. The frozen model misses by two thousand nine hundred and thirty six. The model still '
                          'wins, though by less than on validation. That is a normal and honest result.'},
      'word_icons': {'frozen model': ('ml_r4_icon', {'kind': 'snow'}),
                     'handover': ('ml_r4_icon', {'kind': 'folder2'}),
                     'restart and run all': ('ml_r4_icon', {'kind': 'restart'}),
                     'limit': ('ml_r4_icon', {'kind': 'bounds'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'The locked trips are opened once and reported',
                  'fig': 'ml_open_once',
                  'points': ['Thirty trips stayed locked until now.', 'Open them once.', 'Report whatever number appears.'],
                  'say': 'The thirty locked trips have waited all this time. Now we open them once, with the model already frozen, and write down '
                         'the number.\n'
                         '\n'
                         'If the number is disappointing we report it anyway. Changing the model now and trying again would make the test '
                         'worthless.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'The lead over the plain guess shrinks at the test',
                  'fig': 'ml_val_vs_test',
                  'points': ['Validation lead: 4,361 against 2,255.',
                             'Final test lead: 3,617 against 2,936.',
                             'A smaller lead on fresh trips is normal.'],
                  'say': 'On validation the model beat the plain guess by a wide margin. On the final test the margin is smaller. This happens '
                         'because we chose the model using the validation trips, so it looked a little better there than it really is.\n'
                         '\n'
                         'The final test gives the honest figure.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A handover lets someone else rerun your work',
                  'fig': 'ml_handover_checklist',
                  'points': ['Tick every line before you hand over.'],
                  'say': 'A handover means somebody else can pick up your folder and run it. Keep the data file next to the notebook. Check that '
                         'restart and run all works from the top. State where the data came from, and say that it is invented.\n'
                         '\n'
                         'Report validation and final test separately, and write the limits next to the result.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A one page report has five parts',
                  'fig': 'ml_one_page_report',
                  'points': ['Question, then data and method.', 'Result with the baseline beside it.', 'End with a limit and a next step.'],
                  'say': 'Your report fits on one page. Open with the question. Describe the data and method. Give the result, with the baseline '
                         'beside it so a reader can judge. Add one limit and one next step.\n'
                         '\n'
                         'A stranger should be able to read it in two minutes.'}]},
 23: {'question': {'fig': 'ml_parent_five_slides',
                   'alt': 'Five slide cards in a row: question, data, test, result and limit',
                   'say': 'Your showcase has five slides, one for each of these ideas. The question, the data, the test, the result and the limit. '
                          'Five minutes in all, with no jargon a parent would stumble over. Today you build the five slides and rehearse them with a '
                          'partner.'},
      'word_icons': {'claim': ('ml_r4_icon', {'kind': 'bubble'}),
                     'demonstration': ('ml_r4_icon', {'kind': 'screen'}),
                     'audience': ('ml_r4_icon', {'kind': 'people'}),
                     'backup': ('ml_icon', {'kind': 'copy'}),
                     'disclosure': ('ml_r4_icon', {'kind': 'disclose'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A claim stands on the numbers that support it',
                  'fig': 'ml_claim_evidence',
                  'points': ['State the claim in one sentence.', 'Give the plain guess error.', 'Give the model error beside it.'],
                  'say': 'Start with the claim. The model guesses fares better than a plain guess. Then show the two numbers that support it: the '
                         'plain guess misses by three thousand six hundred and seventeen, the model by two thousand nine hundred and thirty six.\n'
                         '\n'
                         'A claim with no number is only an opinion.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Say the finding in words your listener knows',
                  'fig': 'ml_audience_cards',
                  'points': ['A parent wants the idea.', 'A classmate wants the method.', 'Choose words for the person in front of you.'],
                  'say': 'The finding is the same for everyone. The words change. To a parent you say that it guesses the fare from the distance, '
                         'and was tested on trips it never saw. To a classmate you can name the method.\n'
                         '\n'
                         'Write your sentence for a parent first. If they would understand it, the rest is easy.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Prepare a backup demo and say if AI helped',
                  'fig': 'ml_demo_backup',
                  'points': ['Keep a screenshot of the saved output.', 'Use it if the live run fails.', 'Disclose any AI help on the last slide.'],
                  'say': 'Laptops fail at the worst moments. Keep a screenshot of your saved output, so you can carry on if the live run breaks. And '
                         'if an AI assistant helped you, say so on the last slide.\n'
                         '\n'
                         'Being open about help is part of doing honest work.'}]},
 24: {'question': {'fig': 'ml_showcase_run',
                   'alt': 'Four steps of the showcase: present, explain, answer and make a small change unaided',
                   'say': 'The showcase has four parts. You present your five slides. You explain what the number means. You answer questions from '
                          'the room. Then you make one small change to your own code with nobody helping. This is your chance to show that the work '
                          'is yours and that you understand it.'},
      'word_icons': {'showcase': ('ml_r4_icon', {'kind': 'screen'}),
                     'unaided': ('ml_r4_icon', {'kind': 'solo'}),
                     'completion record': ('ml_r4_icon', {'kind': 'cert'}),
                     'portfolio': ('ml_r4_icon', {'kind': 'folder2'}),
                     'next step': ('ml_r4_icon', {'kind': 'stairs'}),
                     'feedback': ('ml_r4_icon', {'kind': 'bubble'})},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Quote the number you measured when asked',
                  'fig': 'ml_final_test_bars',
                  'points': ['The final test is your evidence.'],
                  'say': 'Questions from the room are easier when you have your numbers ready. The plain guess misses by three thousand six hundred '
                         'and seventeen shillings on the locked trips. Your frozen model misses by two thousand nine hundred and thirty six.\n'
                         '\n'
                         'If you do not know an answer, say so, and say how you would find out.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'One unaided change shows you know your code',
                  'fig': 'ml_unaided_change',
                  'points': ['Change one thing in your own notebook.', 'Predict the result first.', 'Run it and explain the difference.'],
                  'say': 'At the end you change one thing in your own code, perhaps a setting or an input. Say what you expect to happen before you '
                         'run it. Then run it and explain the difference.\n'
                         '\n'
                         'If something breaks, read the last line of the error first. That line usually tells you what to look at.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Your portfolio and your next step go home with you',
                  'fig': 'ml_portfolio_next',
                  'points': ['Keep the notebook, data, report and AI log together.', 'Pick one next step.', 'Ask a new question next time.'],
                  'say': 'Before you leave, collect your portfolio: the handover notebook, the data file, the one page report and your AI use log. '
                         'Keep them in one folder.\n'
                         '\n'
                         'Then choose one next step. A new question, real data used with permission, or a bigger model tested fairly.'}]},
 'F03': {'question': {'fig': 'ml_same_mean_spread',
                      'alt': 'Two groups of four numbers with the same mean of 4 and different spread',
                      'say': 'Group A has the numbers two, two, six and six. Group B has four, four, four and four. Both have a mean of four. Yet '
                             'they are very different groups, because A is spread out and B is not. In this lab you find a number that tells them '
                             'apart, and you meet proportion and probability along the way.'},
         'word_icons': {'mean': ('ml_icon', {'kind': 'level'}),
                     'deviation': ('ml_r4_icon', {'kind': 'dev'}),
                     'standard deviation': ('ml_r4_icon', {'kind': 'sd_band'}),
                     'proportion': ('ml_icon', {'kind': 'pie'}),
                     'probability': ('ml_icon', {'kind': 'die'}),
                     'observed fraction': ('ml_r4_icon', {'kind': 'frac_bar'})},
         'slides': [{'at': 0,
                     'kind': 'concept',
                     'title': 'A deviation is how far a value sits from the mean',
                     'fig': 'ml_deviation_arrows',
                     'points': ['Subtract the mean from each value.',
                                'Below the mean gives a negative number.',
                                'Above the mean gives a positive number.'],
                     'say': 'The mean of two, two, six and six is four. For each value, subtract the mean. Two gives minus two. Six gives plus two. '
                            'These gaps are called deviations, and they can be negative.\n'
                            '\n'
                            'The standard deviation is a typical size of these gaps. For this group it is two.'},
                    {'at': 1,
                     'kind': 'concept',
                     'title': 'A proportion is a part divided by the whole',
                     'fig': 'ml_counters_fraction',
                     'points': ['Three of five counters are blue.', 'Three divided by five is 0.6.', 'Times 100, that is 60 percent.'],
                     'say': 'A bag holds three blue counters and two red ones. The proportion of blue is three out of five, which is zero point six. '
                            'Multiply by a hundred to get sixty percent.\n'
                            '\n'
                            'If each counter is equally likely to be picked, the chance of picking blue is also zero point six.'},
                    {'at': 1,
                     'kind': 'concept',
                     'title': 'What happened in ten throws is not the probability',
                     'fig': 'ml_prob_vs_fraction',
                     'points': ['A fair die has probability 2/6 of showing above 4.',
                                'Ten throws give an observed fraction.',
                                'The fraction need not match.'],
                     'say': 'For a fair die, two faces out of six are above four, so the probability is two sixths. Throw it ten times and you get '
                            'an observed fraction, which can be quite different.\n'
                            '\n'
                            'An observed fraction is an estimate. It does not promise what the next throw will give.'}]},
 'F04': {'question': {'fig': 'ml_weighted_sum',
                      'alt': 'A weighted sum: an intercept, area times its weight and rooms times its weight add up to a predicted rent',
                      'say': 'Here is how a model turns two measurements into one prediction. Start with a fixed amount, the intercept. Add the area '
                             'times its weight. Add the rooms times their weight. The total is the predicted rent. These numbers are invented for '
                             'teaching. A real model learns its weights from examples, but the arithmetic is exactly this.'},
         'word_icons': {'matrix': ('ml_icon', {'kind': 'matrix'}),
                     'shape': ('ml_icon', {'kind': 'shape'}),
                     'weight': ('ml_r4_icon', {'kind': 'slider'}),
                     'weighted sum': ('ml_r4_icon', {'kind': 'wsum'}),
                     'intercept': ('ml_r4_icon', {'kind': 'intercept'}),
                     'slope': ('ml_r4_icon', {'kind': 'rise'})},
         'slides': [{'at': 0,
                     'kind': 'concept',
                     'title': 'A matrix holds one home on every row',
                     'fig': 'ml_matrix_grid',
                     'points': ['Two homes with two measurements each.', 'The shape is 2 by 2.', 'homes[0, 1] means row 0, column 1.'],
                     'say': 'A matrix is a table of numbers. Here each row is one home, with its area in the first column and its number of rooms in '
                            'the second. The shape is rows by columns, so two by two.\n'
                            '\n'
                            'To pick one number, give the row and then the column. Homes zero comma one is the rooms of the first home, which is '
                            'two.'},
                    {'at': 1,
                     'kind': 'concept',
                     'title': 'The slope is the rent gain per extra square metre',
                     'fig': 'ml_slope_step',
                     'points': ['Add one square metre.', 'Keep the rooms the same.', 'The rent rises by 3,000.'],
                     'say': 'Take a home of forty square metres with two rooms. Its rent from the rule is two hundred and sixty thousand. Make it '
                            'forty one square metres, with the rooms unchanged. The rent rises by three thousand.\n'
                            '\n'
                            'That three thousand is the slope for the area.'},
                    {'at': 2,
                     'kind': 'concept',
                     'title': 'A new row is predicted with the same weights',
                     'fig': 'ml_matrix_rows',
                     'points': ['Add the home [50, 2] as a third row.', 'The shape becomes 3 by 2.', 'Its prediction is 290,000.'],
                     'say': 'Add a third home with fifty square metres and two rooms. The matrix now has three rows. The weights do not change, so '
                            'the same rule gives a prediction for the new row: two hundred and ninety thousand shillings.\n'
                            '\n'
                            'Check it on paper. A hundred thousand, plus three thousand times fifty, plus twenty thousand times two.'}]},
 'ML25': {'question': {'fig': 'ml_neuron_net',
                       'alt': 'A small neural network with four inputs, eight hidden units and three outputs',
                       'say': 'This is a small neural network. Four circles on the left take the four flower measurements. Eight hidden circles in '
                              'the middle combine them. Three circles on the right stand for the three species. Each line carries a weight, the same '
                              'kind of number you met in the weighted sum. The question for today is whether this bigger model is worth the extra '
                              'trouble on a small set of flowers.'},
          'word_icons': {},
          'slides': [{'at': 0,
                      'kind': 'wide',
                      'title': 'A network repeats the weighted sum many times',
                      'fig': 'ml_weighted_sum',
                      'points': ['Each line in the network carries a weight like these.'],
                      'say': 'You already know a weighted sum from the matrix lab. Multiply each input by its weight and add the results. A neural '
                             'network does this again and again, with many weights, and the weights are learned from examples.\n'
                             '\n'
                             'Nothing else is hiding inside. It is the same arithmetic, repeated.'},
                     {'at': 0,
                      'kind': 'concept',
                      'title': 'Scaling puts every measurement on a similar footing',
                      'fig': 'ml_scale_inputs',
                      'points': ['Petal length runs wider than petal width.',
                                 'Scaling centres each column on zero.',
                                 'Networks learn badly without it.'],
                      'say': 'The four flower measurements run over different ranges. Petal length covers about six centimetres, petal width only '
                             'about two. A network trains poorly when numbers are on such different scales.\n'
                             '\n'
                             'Scaling moves every column to centre on zero and a similar width, and the network learns much more smoothly.'},
                     {'at': 1,
                      'kind': 'concept',
                      'title': 'Score the network, the tree and the baseline alike',
                      'fig': 'ml_model_trio',
                      'points': ['Same validation flowers for all three.', 'Same accuracy measure.', 'Bigger is not automatically better.'],
                      'say': 'We train three models. The majority baseline, the depth three tree and the small network. Each is scored on the same '
                             'validation flowers with the same accuracy measure.\n'
                             '\n'
                             'On a hundred and fifty flowers a network has no special advantage. A bigger model is not automatically a better one, '
                             'and only a fair comparison can tell.'}]}}
