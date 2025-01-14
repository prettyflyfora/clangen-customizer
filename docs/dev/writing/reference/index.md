# Reference 
This page contains formatting information that is generally utilized across all event formats and should be treated as a main reference.

## Pronoun Tags

There are three kinds of pronoun tag: `PRONOUN`, `VERB` and `ADJ` tags.

#### A note on plural pronouns
Though less relevant in English, the ability to specify plural pronouns is provided. The format is slightly different:
```
{PRONOUN/PLURAL/m_c+r_c/subject/CAP}
{VERB/PLURAL/m_c+r_c/conju_0/conju_1/[...]/conju_n}
{ADJ/PLURAL/m_c+r_c/gender_0/gender_1/[...]/gender_n}
```
The addition of `PLURAL` immediately following the tag identifier signals that it's a plural pronoun and to use the relevant system. Each cat that is to be referred to by the plural must be referenced in this block, separated by a `+`. Otherwise, the system is the same as below for singular pronouns.

### PRONOUN
A `PRONOUN` tag has three main sections: the `PRONOUN` identifier, the relevant cat, and which pronoun is being requested. There is an optional modifier at the end - `CAP` - that is used to signal that the requested pronoun should be capitalized.

Example:
```
{PRONOUN/m_c/subject}
{PRONOUN/m_c/subject/CAP}
```
Permitted pronouns and their English equivalents:

| Pronoun   | English equivalent       |
|-----------|--------------------------|
| `subject` | he/she/they              |
| `object`  | him/her/them             |
| `poss`    | his/her/their            |
| `inposs`  | his/hers/theirs          |
| `self`    | himself/herself/themself |

### VERB
A `VERB` tag has a technically-infinite number of sections depending on the language, but in English it has four sections: the `VERB` identifier, the relevant cat, and the options for each conjugation in the language (in the case of English, plural and singular conjugations).

Example:
```
{VERB/m_c/were/was}
```

!!! caution
    Pay close attention to the order of verbs. In English, **plural conjugation is first**.

### ADJ
Not especially relevant for English, the `ADJ` tag exists to allow items in a sentence to be referred to with the correct grammatical gender. An English example of gendered words could be actor/actress.

Example:
```
{ADJ/m_c/parent/father/mother}
```


## Writing Histories
Cats receive history text to go with each scar-able injury as well as possibly-fatal injury and direct deaths.  These histories show up in their profile.  Many event formats require you to include the history text if a cat is being injured or killed.  These typically refer to three different history types: `scar`, `reg_death`, `lead_death`.  Following are the guidelines for writing each:

| history type | guidelines                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| scar         | This history is given to a cat who gains a scar from an injury gotten during the event.  ONLY INCLUDE if the injury being given is able to scar (i.e a bruise will not scar, but a claw-wound will scar).  This should be a single, full sentence specifying how the cat was scarred.                                                                                                                                                                                                                                                                                                                                                                               |
| reg_death    | This history is given to a non-leader cat who is either killed by the event or dies from an injury gotten during the event.  This should be a single, full sentence specifying how the cat died.  Try not to get too wordy with these.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| lead_death   | This history is given to a leader cat who is either killed by the event or dies from and injury gotten during the event.  This should be a sentence fragment.  Leaders are able to die multiple times, so on their profiles their deaths are listed in one single sentence.  This sentence is formatted as such: "[leader name] lost a life when they [lead_death sentence fragment]" with each following death being added on to create a list with a comma between each item (and the last list item being added with an "and").  Your lead_death text must be able to work within this grammar format and should not include punctuation at the end of the text. |

**Example of acceptable histories**
```json
{
  "scar": "m_c gained a scar from a fox.",
  "reg_death": "m_c died from a fox bite.",
  "lead_death": "died from a fox bite"
}
```

## Tag Lists
Our events generally require writers to "tag" certain attributes.  These "tags" are fairly universal across all events, so the lists are held here to serve as quick reference.

### Conditions and Scars

=== "Taggable Injury Pools"
    
    > | **INJURY POOL NAME** | **INJURIES**                                                            |
    |----------------------|-------------------------------------------------------------------------|
    | `battle_injury`      | `claw-wound`, `cat bite`, `mangled leg`, `mangled tail`, `torn pelt`    |
    | `minor_injury`       | `sprain`, `sore`, `bruises`, `scrapes`                                  |
    | `blunt_force_injury` | `broken bone`, `broken back`, `head damage`, `broken jaw`               |
    | `hot_injury`         | `heat exhaustion`, `heat stroke`, `dehydrated`                          |
    | `cold_injury`        | `shivering`, `"frostbite" `                                               |
    | `big_bite_injury`    | `bite-wound`, `broken bone`, `torn pelt`, `mangled leg`, `mangled tail` |
    | `small_bite_injury`  | `bite-wound`, `torn ear`, `torn pelt`, `scrapes`                        |
    | `beak_bite`          | `beak bite`, `torn ear`, `scrapes`                                      |
    | `rat_bite`           | `rat bite`, `torn ear`, `torn pelt`                                     |

    > If you’d like a patrol to have an injury from one of the injury pools above, use the pool name (i.e. "battle_injury" for injuries from other cats) instead of the injury.  Think we need another pool? Let the senior developers know in the discord developer areas and let's talk.  We can have many pools, there's no limit!


===  "Injuries"

     > | Injuries                 | Allowed within events? | Capable of scarring? |
    |--------------------------|:------------------------:|:----------------------:|
    | `blood loss`             | :x:                    | :x:                  |
    | `tick bites`             | :fontawesome-solid-check:     | :x:                  |
    | `claw-wound`             | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `bite-wound`             | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `cat bite`               | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `beak bite`              | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `snake bite`             | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `quilled by a porcupine` | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `rat bite`               | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `mangled leg`            | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `mangled tail`           | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `broken jaw`             | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `broken bone`            | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `sore`                   | :fontawesome-solid-check:     | :x:                  |
    | `phantom pain`           | :x:                    | :x:                  |
    | `bruises`                | :fontawesome-solid-check:     | :x:                  |
    | `scrapes`                | :fontawesome-solid-check:     | :x:                  |
    | `cracked pads`           | :fontawesome-solid-check:     | :x:                  |
    | `small cut`              | :fontawesome-solid-check:     | :x:                  |
    | `sprain`                 | :fontawesome-solid-check:     | :x:                  |
    | `bee sting`              | :fontawesome-solid-check:     | :x:                  |
    | `joint pain`             | :fontawesome-solid-check:     | :x:                  |
    | `dislocated joint`       | :fontawesome-solid-check:     | :x:                  |
    | `torn pelt`              | :fontawesome-solid-check:     | :x:                  |
    | `torn ear`               | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `water in their lungs`   | :fontawesome-solid-check:     | :x:                  |
    | `shivering`              | :fontawesome-solid-check:     | :x:                  |
    | `frostbite`              | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `burn`                   | :fontawesome-solid-check:     | :x:                  |
    | `severe burn`            | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `shock`                  | :fontawesome-solid-check:     | :x:                  |
    | `lingering shock`        | :fontawesome-solid-check:     | :x:                  |
    | `dehydrated`             | :fontawesome-solid-check:     | :x:                  |
    | `head damage`            | :fontawesome-solid-check:     | :x:                  |
    | `damaged eyes`           | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `broken back`            | :fontawesome-solid-check:     | :fontawesome-solid-check:   |
    | `poisoned`               | :fontawesome-solid-check:     | :x:                  |
    | `headache`               | :fontawesome-solid-check:     | :x:                  |
    | `severe headache`        | :fontawesome-solid-check:     | :x:                  |
    | `pregnant`               | :x:                    | :x:                  |
    | `recovering from birth`  | :x:                    | :x:                  |

===  "Illnesses"

    > | Illness                | Allowed within events? |
    |------------------------|:------------------------:|
    | `fleas`                | :fontawesome-solid-check:     |
    | `seizure`              | :fontawesome-solid-check:     |
    | `diarrhea`             | :fontawesome-solid-check:     |
    | `running nose`         | :fontawesome-solid-check:     |
    | `kittencough`          | :fontawesome-solid-check:     |
    | `whitecough`           | :fontawesome-solid-check:     |
    | `greencough`           | :fontawesome-solid-check:     |
    | `yellowcough`          | :fontawesome-solid-check:     |
    | `redcough`             | :fontawesome-solid-check:     |
    | `an infected wound`    | :x:                    |
    | `a festering wound`    | :x:                    |
    | `carrionplace disease` | :fontawesome-solid-check:     |
    | `heat stroke`          | :fontawesome-solid-check:     |
    | `heat exhaustion`      | :fontawesome-solid-check:     |
    | `stomachache`          | :fontawesome-solid-check:     |
    | `constant nightmares`  | :fontawesome-solid-check:     |
    | `grief stricken`       | :x:                    |
    | `malnourished`         | :x:                    |
    | `starving`             | :x:                    |

===  "Permanent Conditions"

    > !!! important
        Generally we want to avoid giving a permanent condition to a cat, instead we should give them a condition that can lead to permanence (i.e. give 'broken back' instead of 'paralyzed')

    > * `crooked jaw`
    * `lost a leg`
    * `born without a leg`
    * `weak leg`
    * `twisted leg`
    * `lost their tail`
    * `born without a tail`
    * `paralyzed`
    * `raspy lungs`
    * `wasting disease`
    * `blind`
    * `one bad eye`
    * `failing eyesight`
    * `partial hearing loss`
    * `deaf`
    * `constant joint pain`
    * `seizure prone`
    * `allergies`
    * `constantly dizzy`
    * `recurring shock`
    * `lasting grief`
    * `persistent headaches`
    

=== "Scars"

    >`ONE`, `TWO`, `THREE`, `TAILSCAR`, `SNOUT`, `CHEEK`, `SIDE`, `THROAT`, `TAILBASE`, `BELLY`, `LEGBITE`, `NECKBITE`, `FACE`, `MANLEG`, `BRIGHTHEART`, `MANTAIL`, `BRIDGE`, `RIGHTBLIND`, `LEFTBLIND`, `BOTHBLIND`, `BEAKCHEEK`, `BEAKLOWER`, `CATBITE`, `RATBITE`, `QUILLCHUNK`, `QUILLSCRATCH`, `HINDLEG`, `BACK`, `QUILLSIDE`, `SCRATCHSIDE`, `BEAKSIDE`, `CATBITETWO`, `FOUR`, `LEFTEAR`, `RIGHTEAR`, `NOTAIL`, `HALFTAIL`, `NOPAW`, `NOLEFTEAR`, `NORIGHTEAR`, `NOEAR`, `SNAKE`, `TOETRAP`, `BURNPAWS`, `BURNTAIL`, `BURNBELLY`, `BURNRUMP`, `FROSTFACE`, `FROSTTAIL`, `FROSTMITT`, `FROSTSOCK`, `TOE`, `SNAKETWO`

    > !!! tip
        If you would like a visual reference for how each scar appears on the sprite, please check the [Scar Visual Guide](https://docs.google.com/spreadsheets/d/18T-VPGo4GJP35ECYnkzqKZThd6t8j7TwN97QspXtXY0/edit#gid=1080597059).


### Backstories
You can use either the backstory pool name, or an individual backstory name.  When using a backstory pool, please be sure to check that all the backstories contained within will have text suitable for your needs.  You can find the backstory text within `resources/dicts/backstories.json`.

| **BACKSTORY POOL NAMES**     | **BACKSTORIES**                                                                                                                                                                                    |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `clan_founder_backstories`   | `clan_founder`                                                                                                                                                                                     |
| `clanborn_backstories`       | `clanborn`                                                                                                                                                                                         |
| `outsider_roots_backstories` | `outsider_roots1`, `outsider_roots2`                                                                                                                                                               |
| `half_clan_backstories`      | `halfclan1`, `halfclan2`                                                                                                                                                                           |
| `loner_backstories`          | `loner1`, `loner2`, `loner3`, `loner4`, `refugee2`, `tragedy_survivor4`, `guided3`, `refugee5`, `wandering_healer2`                                                                                |
| `rogue_backstories`          | `rogue1`, `rogue2`, `rogue3`, `refugee4`, `tragedy_survivor2`, `guided2`, `refugee5`, `wandering_healer1`                                                                                          |
| `kittypet_backstories`       | `kittypet1`, `kittypet2`, `kittypet3`, `kittypet4`, `refugee3`, `tragedy_survivor3`, `guided1`, `refugee6`                                                                                         |
| `former_clancat_backstories` | `otherclan1`, `otherclan2`, `otherclan3`, `ostracized_warrior`, `disgraced1`, `disgraced2`, `disgraced3`, `retired_leader`, `refugee1`, `tragedy_survivor1`, `medicine_cat`, `guided4`, `refugee5` |
| `healer_backstories`         | `medicine_cat`, `wandering_healer1`, `wandering_healer2`                                                                                                                                           |
| `orphaned_backstories`       | `orphaned1`, `orphaned2`, `orphaned3`, `orphaned4`, `orphaned5`, `orphaned6`                                                                                                                       |
| `abandoned_backstories`      | `abandoned1`, `abandoned2`, `abandoned3`, `abandoned4`                                                                                                                                             |
| `outsider_backstories`       | `outsider1`, `outsider2`, `outsider3`                                                                                                                                                              |

### Age and Status

=== "Ages"

    > * `newborn`
    * `kitten`
    * `adolescent`
    * `young adult`
    * `adult`
    * `senior adult`
    * `senior`

=== "Basic Statuses"

    > * `newborn`
    * `kitten`
    * `apprentice`
    * `mediator apprentice`
    * `medicine cat apprentice`
    * `warrior`
    * `mediator`
    * `medicine cat`
    * `deputy`
    * `leader`
    * `elder`
    * `any`

=== "Life/Death Statuses"

    > * `living`
    * `starclan`
    * `darkforest`
    * `unknownresidence`

=== "Affiliation Statuses"

    > * `kittypet`
    * `loner`
    * `rogue`
    * `former Clancat`
    * `exiled`
    * `lost`
    * `outside cat`
    * `clancat`

!!! important
    
    Not all statuses are utilized in all formats, please check the relevant event format guide for information on what statuses are or are not valid.



### Traits and Skills

=== "Skills"

    > !!! note
        Remember, skills are formatted as `SKILL,#`.  For example, `TEACHER,1` is `quick to help` and `SPEAKER,4` is `eloquent speaker`.

    > | **SKILL,**       | **1**                            | **2**                     | **3**                    | **4**                          |
    |------------------|:----------------------------------:|:---------------------------:|:--------------------------:|:--------------------------------:|
    | **TEACHER**     | `quick to help`                 | `good teacher`           | `great teacher`         | `excellent teacher`           |
    | **HUNTER**      | `moss-ball hunter`              | `good hunter`            | `great hunter`          | `renowned hunter`             |
    | **FIGHTER**     | `avid play-fighter`             | `good fighter`           | `formidable fighter`    | `unusually strong fighter`     |
    | **RUNNER**      | `never sits still`              | `fast runner`            | `incredible runner`     | `fast as the wind`            |
    | **CLIMBER**     | `constantly climbing`           | `good climber`           | `great climber`         | `impressive climber`          |
    | **SWIMMER**     | `splashes in puddles`           | `good swimmer`           | `talented swimmer`      | `fish-like swimmer`           |
    | **SPEAKER**     | `confident with words`          | `good speaker`           | `great speaker`         | `eloquent speaker`            |
    | **MEDIATOR**    | `quick to make peace`           | `good mediator`          | `great mediator`        | `skilled mediator`             |
    | **CLEVER**      | `quick witted`                  | `clever`                 | `very clever`           | `incredibly clever`            |
    | **INSIGHTFUL**  | `careful listener`              | `helpful insight`        | `valuable insight`      | `trusted advisor`              |
    | **SENSE**       | `oddly observant`               | `natural intuition`      | `keen eye`              | `unnatural senses`             |
    | **KIT**         | `active imagination`            | `good kitsitter`         | `great kitsitter`       | `beloved kitsitter`           |
    | **STORY**       | `lover of stories`              | `good storyteller`       | `great storyteller`     | `masterful storyteller`        |
    | **LORE**        | `interested in Clan history`    | `learner of lore`        | `lore keeper`           | `lore master`                  |
    | **CAMP**        | `picky nest builder`            | `steady paws`            | `den builder`           | `camp keeper`                  |
    | **HEALER**      | `interested in herbs`           | `good healer`            | `great healer`          | `fantastic healer`             |
    | **STAR**        | `curious about StarClan`        | `connection to StarClan` | `deep StarClan bond`    | `unshakable StarClan link`    |
    | **DARK**        | `interested in the Dark Forest` | `Dark Forest affinity`   | `deep Dark Forest bond` | `unshakable Dark Forest link` |
    | **OMEN**        | `interested in oddities`        | `omen seeker`            | `omen sense`            | `omen sight`                   |
    | **DREAM**       | `restless sleeper`              | `strange dreamer`        | `dream walker`          | `dream shaper`                 |
    | **CLAIRVOYANT** | `oddly insightful`              | `somewhat clairvoyant`   | `fairly clairvoyant`    | `incredibly clairvoyant`       |
    | **PROPHET**     | `fascinated by prophecies`      | `prophecy seeker`        | `prophecy interpreter`  | `prophet`                      |
    | **GHOST**       | `morbid curiosity`              | `ghost sense`            | `ghost sight`           | `ghost speaker`                |

=== "Traits"

    > !!! note
        See the [trait dictionary](trait-dictionary.md) for further information on each trait and the desired "feel" of the personality.
    >
    >  * `troublesome`
    * `lonesome`
    * `fierce`
    * `bloodthirsty`
    * `cold`
    * `childish`
    * `playful`
    * `charismatic`
    * `bold`
    * `daring`
    * `nervous`
    * `righteous`
    * `insecure`
    * `strict`
    * `compassionate`
    * `thoughtful`
    * `ambitious`
    * `confident`
    * `adventurous`
    * `calm`
    * `careful`
    * `faithful`
    * `loving`
    * `loyal`
    * `responsible`
    * `shameless`
    * `sneaky`
    * `strange`
    * `vengeful`
    * `wise`
    * `arrogant`
    * `competitive`
    * `grumpy`
    * `cunning`
    * `oblivious`
    * `gloomy`
    * `sincere`
    * `flamboyant`
    * `rebellious`


### Snippet Lists
> These abbreviations can be used to insert items from snippet lists into your text. Using an abbr will add 1-3 random items from the given snippet list, formatted as a written list (i.e. `item1, item2, and item3`). 
> 
>The following table also displays certain categories within each snippet list that you can call. To call these categories, you can just add the category after the snippet list abbr, like so: `prophecy_list_sight`.  You can even specify multiple categories, like so: `prophecy_list_sight_touch`.  If you do not add a category, then every category will be used. 

> Full snippet lists are found in `resources/dicts/snippet_collections.json`.  Feel free to add more options into these lists!

| Snippet       | Sight                     | Sound                     | Smell                     | Emotion                   | Touch                     | Taste                     |
|---------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|
| prophecy_list | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :x:                       |
| omen_list     | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :x:                       |
| clair_list    | :x:                       | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: | :fontawesome-solid-check: |
| dream_list    | :x:                       | :x:                       | :x:                       | :x:                       | :x:                       | :x:                       |
| story_list    | :x:                       | :x:                       | :x:                       | :x:                       | :x:                       | :x:                       |


=== "prophecy_list"

    > Use this for amorphous, dreamy concepts.
    
    > | Sense group | Examples                                                                                   |
    |-------------|--------------------------------------------------------------------------------------------|
    | sight       | blood pooling on the ground, a bird's feather, and a ghostly pair of eyes                        |
    | sound       | a kit's mewl, the rushing sound of a river, and a dying promise                                  |
    | smell       | the smell of the medicine-cat den, the scent of someone long dead, and the scent of another Clan |
    | emotional   | the excitement of an apprentice, the feeling of flight, and a half-remembered promise            |
    | touch       | the brush of a pelt against their own, a tail twining with their own, and the warmth of a parent |
    

=== "omen_list"

    > Use this for more physical ideas: odd and meaningful but still grounded in reality.
    
    > | Sense group | Examples                                                                                        |
    |-------------|-------------------------------------------------------------------------------------------------|
    | sight       | a five-pointed leaf, a split acorn, and a dew-covered spider's web                                    |
    | sound       | a whispering on the wind, the sound of a cat no longer there, and the rustle of wind through the grass    |
    | smell       | the scent of spoiled queen's milk, the scent of a long-dead cat, and pine sap scent strong in the air |
    | emotional   | a pervasive feeling of dread, the imprint of fangs on skin, and the feeling of a hidden onlooker      |
    | touch       | the wind whistling past a claw raised in anger, the ache of fatique as eyes close for good, and an endless cold that seeps into their bones                                                                |


=== "clair_list"

    > Use this for amorphous, unclear things that already happened/could happen.
    
    > | Sense group | Examples                                                                                                |
    |-------------|---------------------------------------------------------------------------------------------------------|
    | sound       | the rumble of many paws on the ground, a betrayal on the wind, and distant wails of grief                     |
    | smell       | the smell of kittypet food, the smell of dirt baked by the sun, and a strange acidic scent                    |
    | emotional   | blood spilt in battle, the ache of an elder's bones, and oozing corruption                                    |
    | touch       | deathly still air, tails entwining, and paws heavy with blood                                                 |
    | taste       | the bitter taste of poppy seeds, the lingering taste of iron on the tongue, and the volatile taste of berries |


=== "dream_list"

    > Use this for dreams. These tend to be shorter, one word or phrase ideas.

    > * <i>Examples:</i> faith, excitement, parental pride, wishing on a star


=== "story_list"

    > Use this to pull the name of a story, in the vein of Aesop's Fables. Possible stories are automatically adjusted to the player's biome.

    > * <i>Examples:</i> The Cougar's Claws, The Cat Who Became a Porcupine, The Dead's Token

***